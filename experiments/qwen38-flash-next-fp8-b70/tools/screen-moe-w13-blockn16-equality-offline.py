#!/usr/bin/env python3
"""Is the W13 GEMM at BLOCK_SIZE_N=16 bit-identical to the certified BLOCK_SIZE_N=32?

The N tile decides which output columns a program computes; every output element's K loop
is unchanged, so the accumulation order over K is the same and the result should be
identical. What that argument does not cover is `tl.dot` itself: a [16, 16] tile and a
[16, 32] tile may take different paths through the systolic array, and the order of the
BLOCK_K reduction inside one dot is not something the kernel source fixes.

So this compares the two tilings' outputs elementwise over Q38_ITERS fresh random decode
cases. A handful of calls cannot support a bitwise claim -- a three-call probe once found
zero differences for the swapped accumulator layout and the server disagreed (A290) -- so
run it with hundreds, and treat the server's exact-2K hash as the test of record either way.

  Q38_ITERS=300 PYTHONPATH=<stage>:<overlay> ... screen-moe-w13-blockn16-equality-offline.py
"""
import os

os.environ.setdefault(
    "VLLM_TUNED_CONFIG_FOLDER",
    "/home/steve/llm-optimizations/experiments/qwen38-flash-next-fp8-b70/configs/moe-m1-w13-n32",
)

import torch
from vllm.model_executor.layers.fused_moe.fused_moe import (
    _prepare_expert_assignment,
    dispatch_fused_moe_kernel,
    try_get_optimal_moe_config,
)
from vllm.model_executor.layers.fused_moe.utils import moe_kernel_quantize_input
from vllm.platforms import current_platform
from vllm.triton_utils import tl

device = torch.device("xpu:0")
torch.xpu.set_device(device)
fp8 = current_platform.fp8_dtype()

E_LOCAL, E_GLOBAL, K, N, TOPK, BLK, M = 128, 512, 2560, 640, 10, 128, 1
ITERS = int(os.getenv("Q38_ITERS", "300"))


def bq(w):
    e, r, c = w.shape
    wb = w.view(e, r // BLK, BLK, c // BLK, BLK)
    amax = wb.abs().amax(dim=(2, 4), keepdim=True).clamp_min(1e-6)
    scale = amax / torch.finfo(fp8).max
    q = (wb / scale).clamp(-torch.finfo(fp8).max, torch.finfo(fp8).max).to(fp8)
    return q.view(e, r, c).contiguous(), scale.view(e, r // BLK, c // BLK).float().contiguous()


def main() -> None:
    gd = torch.Generator(device=device).manual_seed(1)
    w1q, w1s = bq(torch.randn(E_LOCAL, 2 * N, K, generator=gd, device=device) / K**0.5)
    em = torch.full((E_GLOBAL,), -1, dtype=torch.int32)
    em[:E_LOCAL] = torch.arange(E_LOCAL, dtype=torch.int32)
    em = em.to(device)
    get_config = try_get_optimal_moe_config(
        w1q.shape, (E_LOCAL, K, N), TOPK, "fp8_w8a8", M, block_shape=[BLK, BLK])
    base = get_config if isinstance(get_config, dict) else get_config(M)
    cfg32 = dict(base, BLOCK_SIZE_N=32)
    cfg16 = dict(base, BLOCK_SIZE_N=16)
    print(f"iters={ITERS} M={M} K={K} 2N={2 * N} topk={TOPK}")
    print(f"  reference {cfg32}")
    print(f"  candidate {cfg16}")

    g = torch.Generator(device="cpu").manual_seed(int(os.getenv("Q38_SEED", "11")))
    diff_calls = diff_elems = total_elems = 0
    worst = 0.0
    first = None
    for i in range(ITERS):
        x = torch.randn(M, K, generator=g).to(torch.bfloat16).to(device)
        router = torch.randn(M, E_GLOBAL, generator=g).to(device)
        tw, ti = torch.topk(torch.softmax(router.float(), -1), TOPK, -1)
        tw = (tw / tw.sum(-1, keepdim=True)).float()
        ti = ti.to(torch.int32)
        xq, xs = moe_kernel_quantize_input(A=x, A_scale=None, quant_dtype=fp8,
                                           per_act_token_quant=False, block_shape=[BLK, BLK])
        sorted_ids, expert_ids, npad = _prepare_expert_assignment(
            ti, base, M, TOPK, E_GLOBAL, em, use_int8_w8a16=False, use_int4_w4a16=False,
            block_shape=[BLK, BLK], ignore_invalid_experts=True)
        outs = {}
        for name, cfg in (("n32", cfg32), ("n16", cfg16)):
            o = torch.zeros((M, TOPK, 2 * N), device=device, dtype=torch.bfloat16)
            dispatch_fused_moe_kernel(
                xq, w1q, o, xs, w1s, None, tw, sorted_ids, expert_ids, npad, False, TOPK, cfg,
                compute_type=tl.bfloat16, use_fp8_w8a8=True, use_int8_w8a8=False,
                use_int8_w8a16=False, use_int4_w4a16=False, per_channel_quant=False,
                block_shape=[BLK, BLK], B_bias=None)
            torch.xpu.synchronize()
            outs[name] = o.clone()
        a, b = outs["n32"], outs["n16"]
        nd = int((a != b).sum())
        total_elems += a.numel()
        diff_elems += nd
        if nd:
            diff_calls += 1
            worst = max(worst, float((a.float() - b.float()).abs().max()))
            if first is None:
                first = (i, nd, int((ti < E_LOCAL).sum()))
    print(f"iters={ITERS} calls_with_any_diff={diff_calls} diff_elements={diff_elems}/{total_elems} "
          f"({100.0 * diff_elems / max(total_elems, 1):.4f}%) max_abs_diff={worst} first={first}")
    print("VERDICT:", "bit-identical over this sample" if diff_calls == 0 else "NOT bit-identical")


if __name__ == "__main__":
    main()
