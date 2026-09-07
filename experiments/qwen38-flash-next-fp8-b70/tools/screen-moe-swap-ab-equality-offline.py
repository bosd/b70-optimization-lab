#!/usr/bin/env python3
"""Bitwise-equality probe for the swapped MoE accumulator layout (VLLM_XPU_MOE_SWAP_AB).

Runs the decode-shaped block-FP8 fused_experts call twice per iteration, once with the
default layout and once with the swapped one, over Q38_ITERS fresh random inputs and
routings, and reports how often any element differs.

The iteration count is the point. A first version of this probe compared three calls,
found zero differing elements, and was contradicted by the server (A290, hash moved):
at 300 iterations 22 calls differ, 0.2% of elements, by one bf16 step. A handful of
calls cannot support a bitwise claim about a kernel-shape change; the server exact-2K
hash over 2048 generated tokens remains the test of record, and this is only a cheap
pre-filter that must be run with hundreds of iterations to mean anything.

  Q38_ITERS=300 PYTHONPATH=<stage>:<overlay> ... screen-moe-swap-ab-equality-offline.py
"""
import os

os.environ.setdefault("VLLM_TUNED_CONFIG_FOLDER", "/home/steve/llm-optimizations/experiments/qwen38-flash-next-fp8-b70/configs/moe-m1-w13-n32")
os.environ["VLLM_XPU_MOE_SWAP_AB"] = ""
import torch
from vllm.platforms import current_platform
import vllm._custom_ops  # noqa: F401
from vllm.model_executor.layers.fused_moe.fused_moe import fused_experts
from vllm.model_executor.layers.fused_moe.config import fp8_w8a8_moe_quant_config

device = torch.device("xpu:0"); torch.xpu.set_device(device)
E_LOCAL, E_GLOBAL, K, N, TOPK, BLK = 128, 512, 2560, 640, 10, 128
fp8 = current_platform.fp8_dtype(); gd = torch.Generator(device=device).manual_seed(1)
def bq(w):
    e, r, c = w.shape; wb = w.view(e, r // BLK, BLK, c // BLK, BLK)
    amax = wb.abs().amax(dim=(2, 4), keepdim=True).clamp_min(1e-6); scale = amax / torch.finfo(fp8).max
    q = (wb / scale).clamp(-torch.finfo(fp8).max, torch.finfo(fp8).max).to(fp8)
    return q.view(e, r, c).contiguous(), scale.view(e, r // BLK, c // BLK).float().contiguous()
w1q, w1s = bq(torch.randn(E_LOCAL, 2*N, K, generator=gd, device=device)/K**0.5)
w2q, w2s = bq(torch.randn(E_LOCAL, K, N, generator=gd, device=device)/N**0.5)
qc = fp8_w8a8_moe_quant_config(w1_scale=w1s, w2_scale=w2s, block_shape=[BLK, BLK])
em = torch.full((E_GLOBAL,), -1, dtype=torch.int32); em[:E_LOCAL] = torch.arange(E_LOCAL, dtype=torch.int32); em = em.to(device)
g = torch.Generator(device="cpu").manual_seed(int(os.getenv("Q38_SEED", "11")))
ITERS = int(os.getenv("Q38_ITERS", "300"))
ndiff_calls = 0; total_elems = 0; diff_elems = 0; worst = 0.0; first = None
for i in range(ITERS):
    M = 1
    x = torch.randn(M, K, generator=g).to(torch.bfloat16).to(device)
    router = torch.randn(M, E_GLOBAL, generator=g).to(device)
    tw, ti = torch.topk(torch.softmax(router.float(), -1), TOPK, -1)
    tw = (tw / tw.sum(-1, keepdim=True)).float(); ti = ti.to(torch.int32)
    outs = {}
    for mode in ("off", "on"):
        os.environ["VLLM_XPU_MOE_SWAP_AB"] = "1" if mode == "on" else ""
        o = fused_experts(x, w1q, w2q, tw, ti, global_num_experts=E_GLOBAL, expert_map=em, quant_config=qc)
        torch.xpu.synchronize(); outs[mode] = o.clone()
    a, b = outs["off"], outs["on"]
    nd = int((a != b).sum()); total_elems += a.numel(); diff_elems += nd
    if nd:
        ndiff_calls += 1; worst = max(worst, float((a.float()-b.float()).abs().max()))
        if first is None: first = (i, nd, int((ti < E_LOCAL).sum()))
os.environ["VLLM_XPU_MOE_SWAP_AB"] = ""
print(f"iters={ITERS} calls_with_any_diff={ndiff_calls} diff_elements={diff_elems}/{total_elems} "
      f"({100.0*diff_elems/max(total_elems,1):.4f}%) max_abs_diff={worst} first={first}")
