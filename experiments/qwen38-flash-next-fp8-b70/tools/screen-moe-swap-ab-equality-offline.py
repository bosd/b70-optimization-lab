#!/usr/bin/env python3
"""Bitwise-equality probe for the swapped MoE accumulator layout (VLLM_XPU_MOE_SWAP_AB).

Runs the decode-shaped block-FP8 fused_experts call twice in one process, once with the
default layout and once with the swapped one, and compares the outputs bit for bit. The
gate is read per call, so a single process can flip it. Timing is deliberately NOT the
point here (the isolated harnesses do not represent the server's launch path — A282/A286);
this answers only the exactness question before a server screen is spent.

  PYTHONPATH=<stage>:<overlay> ... screen-moe-swap-ab-equality-offline.py
"""
import os

os.environ.setdefault(
    "VLLM_TUNED_CONFIG_FOLDER",
    "/home/steve/llm-optimizations/experiments/qwen38-flash-next-fp8-b70/configs/moe-m1-w13-n32",
)
os.environ["VLLM_XPU_MOE_SWAP_AB"] = ""

import torch  # noqa: E402
from vllm.platforms import current_platform  # noqa: E402
import vllm._custom_ops  # noqa: F401,E402
from vllm.model_executor.layers.fused_moe.fused_moe import fused_experts  # noqa: E402
from vllm.model_executor.layers.fused_moe.config import (  # noqa: E402
    fp8_w8a8_moe_quant_config,
)

device = torch.device("xpu:0")
torch.xpu.set_device(device)
E_LOCAL, E_GLOBAL, K, N, TOPK, BLK = 128, 512, 2560, 640, 10, 128
fp8 = current_platform.fp8_dtype()
gd = torch.Generator(device=device).manual_seed(1)


def bq(w):
    e, r, c = w.shape
    wb = w.view(e, r // BLK, BLK, c // BLK, BLK)
    amax = wb.abs().amax(dim=(2, 4), keepdim=True).clamp_min(1e-6)
    scale = amax / torch.finfo(fp8).max
    q = (wb / scale).clamp(-torch.finfo(fp8).max, torch.finfo(fp8).max).to(fp8)
    return q.view(e, r, c).contiguous(), scale.view(e, r // BLK, c // BLK).float().contiguous()


w1q, w1s = bq(torch.randn(E_LOCAL, 2 * N, K, generator=gd, device=device) / K**0.5)
w2q, w2s = bq(torch.randn(E_LOCAL, K, N, generator=gd, device=device) / N**0.5)
qc = fp8_w8a8_moe_quant_config(w1_scale=w1s, w2_scale=w2s, block_shape=[BLK, BLK])
em = torch.full((E_GLOBAL,), -1, dtype=torch.int32)
em[:E_LOCAL] = torch.arange(E_LOCAL, dtype=torch.int32)
em = em.to(device)

g = torch.Generator(device="cpu").manual_seed(2)
results = {}
for label, M, all_local in (("M1-ep-like", 1, False), ("M1-all-local", 1, True), ("M2-ep-like", 2, False)):
    x = torch.randn(M, K, generator=g).to(torch.bfloat16).to(device)
    router = torch.randn(M, E_GLOBAL, generator=g).to(device)
    if all_local:
        router[:, E_LOCAL:] -= 100
    tw, ti = torch.topk(torch.softmax(router.float(), -1), TOPK, -1)
    tw = (tw / tw.sum(-1, keepdim=True)).float()
    ti = ti.to(torch.int32)
    outs = {}
    for mode in ("off", "on"):
        os.environ["VLLM_XPU_MOE_SWAP_AB"] = "1" if mode == "on" else ""
        out = fused_experts(
            x, w1q, w2q, tw, ti, global_num_experts=E_GLOBAL, expert_map=em, quant_config=qc
        )
        torch.xpu.synchronize()
        outs[mode] = out.clone()
    a, b = outs["off"], outs["on"]
    same = bool(torch.equal(a, b))
    diff = (a.float() - b.float()).abs()
    ndiff = int((a != b).sum())
    results[label] = {
        "bit_identical": same,
        "elements": a.numel(),
        "differing_elements": ndiff,
        "max_abs_diff": float(diff.max()),
        "local_hits": int((ti < E_LOCAL).sum()),
        "routed_slots": M * TOPK,
    }
    print(label, results[label], flush=True)

os.environ["VLLM_XPU_MOE_SWAP_AB"] = ""
print("SWAP_AB bit-identical everywhere:", all(r["bit_identical"] for r in results.values()))
