#!/usr/bin/env python3
"""Where does the MoE step's non-GEMM time go at decode shape?

The step decomposition put the MoE layer at 15.1 ms of a 31.4 ms step, of which the two
GEMMs are 11.9 ms and everything around them is 3.2 ms — 67 us per layer across 48 layers.
At M=1 every one of those surrounding ops is tiny, so the cost is unlikely to be
arithmetic; it is more likely the number of separate kernels. This probe times each stage
of `fused_experts_impl` separately under XPU graph replay of a 48-layer step, so the 67 us
can be attributed before anything is built.

Stages, in the order the decode path runs them:
  quantize1   moe_kernel_quantize_input on the hidden states
  assign      _prepare_expert_assignment (moe_align_block_size: the sort and scatter)
  gemm1       the w13 GEMM
  activation  apply_moe_activation (SiLU and multiply)
  quantize2   moe_kernel_quantize_input on the intermediate
  gemm2       the w2 GEMM
  reduce      ops.moe_sum over the top-k outputs

Isolated harnesses have twice failed to predict this server (A282, A286), so treat this as
attribution to aim the next lever, not as a measurement of the server's step.

  PYTHONPATH=<stage>:<overlay> ... probe-moe-surround-decode-offline.py
"""
import os
import time

os.environ.setdefault(
    "VLLM_TUNED_CONFIG_FOLDER",
    "/home/steve/llm-optimizations/experiments/qwen38-flash-next-fp8-b70/configs/moe-m1-w13-n32",
)

import torch
from vllm import _custom_ops as ops
from vllm.model_executor.layers.fused_moe.config import fp8_w8a8_moe_quant_config
from vllm.model_executor.layers.fused_moe.fused_moe import (
    _prepare_expert_assignment,
    apply_moe_activation,
    dispatch_fused_moe_kernel,
    try_get_optimal_moe_config,
)
from vllm.model_executor.layers.fused_moe.activation import MoEActivation
from vllm.model_executor.layers.fused_moe.utils import moe_kernel_quantize_input
from vllm.platforms import current_platform
from vllm.triton_utils import tl

device = torch.device("xpu:0")
torch.xpu.set_device(device)
fp8 = current_platform.fp8_dtype()

E_LOCAL = int(os.getenv("Q38_PROBE_E", "128"))
E_GLOBAL = int(os.getenv("Q38_PROBE_EG", "512"))
K = int(os.getenv("Q38_PROBE_K", "2560"))
N = int(os.getenv("Q38_PROBE_N", "640"))
TOPK = int(os.getenv("Q38_PROBE_TOPK", "10"))
BLK = 128
M = 1
LAYERS = int(os.getenv("Q38_PROBE_LAYERS", "48"))
REPS = int(os.getenv("Q38_PROBE_REPS", "20"))


def bq(w):
    e, r, c = w.shape
    wb = w.view(e, r // BLK, BLK, c // BLK, BLK)
    amax = wb.abs().amax(dim=(2, 4), keepdim=True).clamp_min(1e-6)
    scale = amax / torch.finfo(fp8).max
    q = (wb / scale).clamp(-torch.finfo(fp8).max, torch.finfo(fp8).max).to(fp8)
    return q.view(e, r, c).contiguous(), scale.view(e, r // BLK, c // BLK).float().contiguous()


def timed(label, fn, results):
    for _ in range(3):
        fn()
    torch.xpu.synchronize()
    try:
        graph = torch.xpu.XPUGraph()
        with torch.xpu.graph(graph):
            for _ in range(LAYERS):
                fn()
        torch.xpu.synchronize()
        graph.replay()
        torch.xpu.synchronize()
        t0 = time.perf_counter()
        for _ in range(REPS):
            graph.replay()
        torch.xpu.synchronize()
        dt = (time.perf_counter() - t0) / REPS
        results.append((label, dt))
        print(f"  {label:11s} {dt * 1e3:8.3f} ms per {LAYERS} layers  ({dt * 1e6 / LAYERS:7.2f} us per layer)")
    except Exception as exc:
        print(f"  {label:11s} graph unavailable ({type(exc).__name__}: {str(exc)[:90]})")


def main() -> None:
    gd = torch.Generator(device=device).manual_seed(1)
    w1q, w1s = bq(torch.randn(E_LOCAL, 2 * N, K, generator=gd, device=device) / K**0.5)
    w2q, w2s = bq(torch.randn(E_LOCAL, K, N, generator=gd, device=device) / N**0.5)
    qc = fp8_w8a8_moe_quant_config(w1_scale=w1s, w2_scale=w2s, block_shape=[BLK, BLK])

    g = torch.Generator(device="cpu").manual_seed(7)
    x = torch.randn(M, K, generator=g).to(torch.bfloat16).to(device)
    router = torch.randn(M, E_GLOBAL, generator=g).to(device)
    tw, ti = torch.topk(torch.softmax(router.float(), -1), TOPK, -1)
    tw = (tw / tw.sum(-1, keepdim=True)).float()
    ti = ti.to(torch.int32)
    em = torch.full((E_GLOBAL,), -1, dtype=torch.int32)
    em[:E_LOCAL] = torch.arange(E_LOCAL, dtype=torch.int32)
    em = em.to(device)

    get_config = try_get_optimal_moe_config(
        w1q.shape, w2q.shape, TOPK, "fp8_w8a8", M, block_shape=[BLK, BLK]
    )
    config = get_config if isinstance(get_config, dict) else get_config(M)
    # The certified per-phase map tiles W13 at BLOCK_SIZE_N=32 and W2 at 64; using one
    # config for both understates W13's speed by mis-tiling it.
    w13_config = dict(config)
    w13_config["BLOCK_SIZE_N"] = int(os.getenv("Q38_PROBE_W13_N", "32"))
    w2_config = dict(config)
    w2_config["BLOCK_SIZE_N"] = int(os.getenv("Q38_PROBE_W2_N", str(config["BLOCK_SIZE_N"])))
    if os.getenv("Q38_PROBE_WARPS"):
        w13_config["num_warps"] = w2_config["num_warps"] = int(os.environ["Q38_PROBE_WARPS"])
    if os.getenv("Q38_PROBE_STAGES"):
        w13_config["num_stages"] = w2_config["num_stages"] = int(os.environ["Q38_PROBE_STAGES"])
    print(f"M={M} E_local={E_LOCAL} K={K} N={N} topk={TOPK} layers={LAYERS}")
    print(f"  w13 config={w13_config}")
    print(f"  w2  config={w2_config}")

    ic1 = torch.empty((M, TOPK, 2 * N), device=device, dtype=torch.bfloat16)
    ic2 = torch.empty((M * TOPK, N), device=device, dtype=torch.bfloat16)
    ic3 = torch.empty((M, TOPK, K), device=device, dtype=torch.bfloat16)
    out = torch.empty_like(x)

    xq, xs = moe_kernel_quantize_input(A=x, A_scale=None, quant_dtype=fp8,
                                       per_act_token_quant=False, block_shape=[BLK, BLK])
    sorted_ids, expert_ids, npad = _prepare_expert_assignment(
        ti, config, M, TOPK, E_GLOBAL, em, use_int8_w8a16=False, use_int4_w4a16=False,
        block_shape=[BLK, BLK], ignore_invalid_experts=True)
    assert config["BLOCK_SIZE_M"] == w13_config["BLOCK_SIZE_M"], "assignment is shared, so M must match"
    i2q, i2s = moe_kernel_quantize_input(A=ic2, A_scale=None, quant_dtype=fp8,
                                         per_act_token_quant=False, block_shape=[BLK, BLK])

    results: list[tuple[str, float]] = []
    print("stage timings under graph replay:")
    timed("quantize1", lambda: moe_kernel_quantize_input(
        A=x, A_scale=None, quant_dtype=fp8, per_act_token_quant=False, block_shape=[BLK, BLK]), results)
    timed("assign", lambda: _prepare_expert_assignment(
        ti, config, M, TOPK, E_GLOBAL, em, use_int8_w8a16=False, use_int4_w4a16=False,
        block_shape=[BLK, BLK], ignore_invalid_experts=True), results)
    timed("gemm1", lambda: dispatch_fused_moe_kernel(
        xq, w1q, ic1, xs, w1s, None, tw, sorted_ids, expert_ids, npad, False, TOPK, w13_config,
        compute_type=tl.bfloat16, use_fp8_w8a8=True, use_int8_w8a8=False, use_int8_w8a16=False,
        use_int4_w4a16=False, per_channel_quant=False, block_shape=[BLK, BLK], B_bias=None), results)
    timed("activation", lambda: apply_moe_activation(MoEActivation.SILU, ic2, ic1.view(-1, 2 * N)), results)
    timed("quantize2", lambda: moe_kernel_quantize_input(
        A=ic2, A_scale=None, quant_dtype=fp8, per_act_token_quant=False, block_shape=[BLK, BLK]), results)
    timed("gemm2", lambda: dispatch_fused_moe_kernel(
        i2q, w2q, ic3, i2s, w2s, None, tw, sorted_ids, expert_ids, npad, True, 1, w2_config,
        compute_type=tl.bfloat16, use_fp8_w8a8=True, use_int8_w8a8=False, use_int8_w8a16=False,
        use_int4_w4a16=False, per_channel_quant=False, block_shape=[BLK, BLK], B_bias=None), results)
    timed("reduce", lambda: ops.moe_sum(ic3.view(*ic3.size()), out), results)

    if results:
        total = sum(dt for _, dt in results)
        gemm = sum(dt for label, dt in results if label.startswith("gemm"))
        print(f"\ntotal {total * 1e3:.3f} ms per {LAYERS} layers; GEMMs {gemm * 1e3:.3f} ms "
              f"({100.0 * gemm / total:.1f}%), surround {(total - gemm) * 1e3:.3f} ms "
              f"({(total - gemm) * 1e6 / LAYERS:.2f} us per layer)")
        for label, dt in sorted(results, key=lambda r: -r[1]):
            print(f"  {label:11s} {100.0 * dt / total:5.1f}% of the modelled step")


if __name__ == "__main__":
    main()
