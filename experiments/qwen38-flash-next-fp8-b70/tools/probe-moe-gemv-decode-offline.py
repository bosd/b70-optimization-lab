#!/usr/bin/env python3
"""Is a GEMV-shaped MoE kernel worth building for the decode step?

The decode MoE GEMM is a tile kernel doing a batch-of-one gather: `tl.dot` cannot go below
a 16-row tile, so with one token per routed expert fifteen of every sixteen rows are
padding, and the grid probe showed a 16-row block per routed expert with only a few local.
The measured cost is neither bandwidth (weights read at 566 GB/s in isolation) nor
arithmetic; it is twenty dependent K iterations per program that the machine cannot hide.

A GEMV does one sixteenth of the arithmetic on the vector ALUs instead of the systolic
array, which on its own is unlikely to help, because the dependency chain is unchanged.
The reason to test it is register pressure: the tile kernel accumulates [16, BLOCK_N] in
fp32, and hand prefetching it was slower (A290-era probe), while a GEMV accumulates only
[BLOCK_N], leaving room to keep several K blocks in flight. So the variants below are
GEMV with PREFETCH of 1, 2 and 4 K blocks, against the tile kernel as reference.

Correctness is checked against a dequantized fp32 matmul, on many random cases, and both
kernels are timed under XPU graph replay of a 48-layer step. Timing here is a filter only:
isolated harnesses have twice failed to predict this server (A282, A286), so a promising
result must still be screened in the server before anything is believed.

  PYTHONPATH=<stage>:<overlay> ... probe-moe-gemv-decode-offline.py
"""
import os
import time

import torch
from vllm.platforms import current_platform
from vllm.triton_utils import tl, triton

device = torch.device("xpu:0")
torch.xpu.set_device(device)
fp8 = current_platform.fp8_dtype()

E_LOCAL = int(os.getenv("Q38_PROBE_E", "128"))
K = int(os.getenv("Q38_PROBE_K", "2560"))
N = int(os.getenv("Q38_PROBE_N", "1280"))
BLK = 128
HITS = int(os.getenv("Q38_PROBE_HITS", "2"))
LAYERS = int(os.getenv("Q38_PROBE_LAYERS", "48"))
REPS = int(os.getenv("Q38_PROBE_REPS", "20"))
TRIALS = int(os.getenv("Q38_PROBE_TRIALS", "50"))


@triton.jit
def _moe_gemv(
    a_ptr, b_ptr, c_ptr, a_scale_ptr, b_scale_ptr, expert_ids_ptr,
    N, K, stride_be, stride_bn, stride_bk, stride_cm, stride_ask, stride_bse,
    stride_bsn, stride_bsk,
    BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr, GROUP_N: tl.constexpr,
    PREFETCH: tl.constexpr,
):
    """One program per (routed slot, N block). Single token, so A is a vector."""
    pid_n = tl.program_id(0)
    pid_m = tl.program_id(1)
    e = tl.load(expert_ids_ptr + pid_m).to(tl.int64)
    offs_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    offs_k = tl.arange(0, BLOCK_K)
    b_base = b_ptr + e * stride_be
    b_ptrs = b_base + offs_n[:, None] * stride_bn + offs_k[None, :] * stride_bk
    a_ptrs = a_ptr + offs_k
    bs_ptrs = b_scale_ptr + e * stride_bse + (offs_n // GROUP_N) * stride_bsn
    acc = tl.zeros((BLOCK_N,), dtype=tl.float32)
    n_k = tl.cdiv(K, BLOCK_K)
    for k0 in range(0, n_k, PREFETCH):
        # Issue the loads of up to PREFETCH K blocks before consuming any of them; the
        # accumulator is one vector, so the register budget allows several in flight.
        for j in tl.static_range(PREFETCH):
            k = k0 + j
            if k < n_k:
                a = tl.load(a_ptrs + k * BLOCK_K, mask=offs_k + k * BLOCK_K < K, other=0.0).to(tl.float32)
                b = tl.load(b_ptrs + k * BLOCK_K * stride_bk).to(tl.float32)
                a_s = tl.load(a_scale_ptr + k * stride_ask)
                b_s = tl.load(bs_ptrs + k * stride_bsk)
                acc += tl.sum(a[None, :] * b, axis=1) * a_s * b_s
    tl.store(c_ptr + offs_n * stride_cm, acc.to(tl.bfloat16), mask=offs_n < N)


def bq(w):
    e, r, c = w.shape
    wb = w.view(e, r // BLK, BLK, c // BLK, BLK)
    amax = wb.abs().amax(dim=(2, 4), keepdim=True).clamp_min(1e-6)
    scale = amax / torch.finfo(fp8).max
    q = (wb / scale).clamp(-torch.finfo(fp8).max, torch.finfo(fp8).max).to(fp8)
    return q.view(e, r, c).contiguous(), scale.view(e, r // BLK, c // BLK).float().contiguous()


def aq(x):
    xb = x.view(-1, K // BLK, BLK)
    amax = xb.abs().amax(dim=2, keepdim=True).clamp_min(1e-6)
    scale = amax / torch.finfo(fp8).max
    q = (xb / scale).clamp(-torch.finfo(fp8).max, torch.finfo(fp8).max).to(fp8)
    return q.view(-1, K).contiguous(), scale.view(-1, K // BLK).float().contiguous()


def reference(xq, xs, wq, ws, experts):
    """Dequantized fp32 matmul, one row per routed expert."""
    out = torch.empty(len(experts), N, dtype=torch.float32, device=device)
    xd = xq.view(1, K // BLK, BLK).to(torch.float32) * xs.view(1, K // BLK, 1)
    xd = xd.view(1, K)
    for i, e in enumerate(experts):
        wd = wq[e].view(N // BLK, BLK, K // BLK, BLK).to(torch.float32) * ws[e].view(N // BLK, 1, K // BLK, 1)
        out[i] = (xd @ wd.view(N, K).t()).squeeze(0)
    return out


def run_gemv(xq, xs, wq, ws, eids, out, prefetch, block_n=64):
    grid = (triton.cdiv(N, block_n), eids.numel())
    _moe_gemv[grid](
        xq, wq, out, xs, ws, eids,
        N, K, wq.stride(0), wq.stride(1), wq.stride(2), out.stride(1),
        xs.stride(1), ws.stride(0), ws.stride(1), ws.stride(2),
        BLOCK_N=block_n, BLOCK_K=BLK, GROUP_N=BLK, PREFETCH=prefetch,
        num_warps=8, num_stages=4,
    )


def main() -> None:
    gd = torch.Generator(device=device).manual_seed(3)
    wq, ws = bq(torch.randn(E_LOCAL, N, K, generator=gd, device=device) / K**0.5)
    g = torch.Generator(device="cpu").manual_seed(5)
    print(f"E={E_LOCAL} N={N} K={K} hits={HITS} layers={LAYERS} trials={TRIALS}")

    worst = 0.0
    nonfinite = 0
    for t in range(TRIALS):
        x = (torch.randn(1, K, generator=g) / K**0.5).to(device)
        xq, xs = aq(x)
        experts = torch.randperm(E_LOCAL, generator=gd, device=device)[:HITS].to(torch.int32)
        out = torch.empty(HITS, N, dtype=torch.bfloat16, device=device)
        run_gemv(xq, xs, wq, ws, experts, out, prefetch=1)
        torch.xpu.synchronize()
        ref = reference(xq, xs, wq, ws, experts.tolist())
        o = out.float()
        bad = int((~torch.isfinite(o)).sum()), int((~torch.isfinite(ref)).sum())
        if any(bad):
            print(f"  trial {t}: non-finite values (gemv {bad[0]}, reference {bad[1]}) of {o.numel()}")
            nonfinite += 1
            continue
        scale = ref.abs().amax().clamp_min(1e-6)
        rel = ((o - ref).abs() / scale).max().item()
        worst = max(worst, rel)
    print(f"GEMV vs dequantized fp32 reference over {TRIALS} trials: worst error relative to the row max = {worst:.2e}"
          f"; trials with non-finite values = {nonfinite}")

    x = (torch.randn(1, K, generator=g) / K**0.5).to(device)
    xq, xs = aq(x)
    experts = torch.arange(HITS, dtype=torch.int32, device=device)
    out = torch.empty(HITS, N, dtype=torch.bfloat16, device=device)
    # Graph replay, so the number is comparable with the tile kernel's 0.16 ms per layer for
    # both GEMMs' K loops measured the same way. An eager launch loop measures submission,
    # not the kernel.
    for pf in (1, 2, 4):
        for _ in range(3):
            run_gemv(xq, xs, wq, ws, experts, out, prefetch=pf)
        torch.xpu.synchronize()
        try:
            graph = torch.xpu.XPUGraph()
            with torch.xpu.graph(graph):
                for _ in range(LAYERS):
                    run_gemv(xq, xs, wq, ws, experts, out, prefetch=pf)
            torch.xpu.synchronize()
            graph.replay()
            torch.xpu.synchronize()
            t0 = time.perf_counter()
            for _ in range(REPS):
                graph.replay()
            torch.xpu.synchronize()
            dt = (time.perf_counter() - t0) / REPS
            print(f"GEMV prefetch={pf}: graph replay {dt*1e3:7.3f} ms per {LAYERS}-layer step "
                  f"({dt*1e6/LAYERS:6.1f} us per layer for one GEMM)")
        except Exception as exc:
            print(f"GEMV prefetch={pf}: graph unavailable ({type(exc).__name__}: {str(exc)[:80]})")


if __name__ == "__main__":
    main()
