#!/usr/bin/env python3
"""Why the MoE GEMM reads expert weights at ~61 GB/s: layout, or bytes in flight?

The decode GEMM reads a [BLOCK_N, BLOCK_K] tile of a [E, N, K] fp8 tensor, which is
BLOCK_N separate 128-byte segments one expert-row apart. Three kernels read exactly the
same number of bytes with the same grid, differing only in the address mapping and in how
many loads each program has outstanding:

  strided    the kernel's pattern today: BLOCK_N segments of BLOCK_K bytes, stride K
  contig     the same bytes from a pre-tiled copy, fully contiguous per program
  strided2   the kernel's pattern with two K-blocks in flight per iteration

If contig is much faster, a load-time repack into tile-contiguous order is the lever, and
it is bit-identical because it moves bytes without touching values or the accumulation
order. If contig matches strided, the ceiling is memory-level parallelism instead, and the
answer is more outstanding loads per program rather than a new layout.

Card 0 only, and it allocates ~1 GiB: do not run it while a server holds the cards.

  PYTHONPATH=<stage>:<overlay> ... probe-moe-weight-read-bandwidth-offline.py
"""
import os
import time

import torch
from vllm.triton_utils import tl, triton

device = torch.device("xpu:0")
torch.xpu.set_device(device)

N = int(os.getenv("Q38_PROBE_N", "1280"))
K = int(os.getenv("Q38_PROBE_K", "2560"))
E = int(os.getenv("Q38_PROBE_E", "96"))  # ~2 experts x 48 layers of one step's w13 reads
BLOCK_N = int(os.getenv("Q38_PROBE_BN", "32"))
BLOCK_K = 128
REPS = int(os.getenv("Q38_PROBE_REPS", "20"))


@triton.jit
def _strided(b_ptr, out_ptr, stride_e, stride_n, NUM_K: tl.constexpr,
             BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr):
    pid = tl.program_id(0)
    e = tl.program_id(1)
    offs_n = pid * BLOCK_N + tl.arange(0, BLOCK_N)
    offs_k = tl.arange(0, BLOCK_K)
    ptrs = b_ptr + e * stride_e + offs_n[:, None] * stride_n + offs_k[None, :]
    acc = tl.zeros((BLOCK_N, BLOCK_K), dtype=tl.float32)
    for _ in range(NUM_K):
        acc += tl.load(ptrs).to(tl.float32)
        ptrs += BLOCK_K
    tl.store(out_ptr + e * tl.num_programs(0) + pid, tl.sum(tl.sum(acc, 1), 0))


@triton.jit
def _strided2(b_ptr, out_ptr, stride_e, stride_n, NUM_K: tl.constexpr,
              BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr):
    pid = tl.program_id(0)
    e = tl.program_id(1)
    offs_n = pid * BLOCK_N + tl.arange(0, BLOCK_N)
    offs_k = tl.arange(0, BLOCK_K)
    ptrs = b_ptr + e * stride_e + offs_n[:, None] * stride_n + offs_k[None, :]
    acc = tl.zeros((BLOCK_N, BLOCK_K), dtype=tl.float32)
    for _ in range(NUM_K // 2):
        a = tl.load(ptrs)
        b = tl.load(ptrs + BLOCK_K)
        acc += a.to(tl.float32) + b.to(tl.float32)
        ptrs += 2 * BLOCK_K
    tl.store(out_ptr + e * tl.num_programs(0) + pid, tl.sum(tl.sum(acc, 1), 0))


@triton.jit
def _contig(b_ptr, out_ptr, stride_e, TILE: tl.constexpr, NUM_K: tl.constexpr):
    pid = tl.program_id(0)
    e = tl.program_id(1)
    base = b_ptr + e * stride_e + pid * TILE * NUM_K
    acc = tl.zeros((TILE,), dtype=tl.float32)
    for i in range(NUM_K):
        acc += tl.load(base + i * TILE + tl.arange(0, TILE)).to(tl.float32)
    tl.store(out_ptr + e * tl.num_programs(0) + pid, tl.sum(acc, 0))


def run(fn, grid, args, label, nbytes):
    for _ in range(3):
        fn[grid](*args)
    torch.xpu.synchronize()
    t0 = time.perf_counter()
    for _ in range(REPS):
        fn[grid](*args)
    torch.xpu.synchronize()
    dt = (time.perf_counter() - t0) / REPS
    print(f"{label:10s} {dt*1e3:8.3f} ms  {nbytes/dt/1e9:7.1f} GB/s")
    return dt


def main() -> None:
    w = torch.randint(0, 255, (E, N, K), dtype=torch.uint8, device=device)
    nbytes = w.numel()
    n_blocks = N // BLOCK_N
    out = torch.zeros(E * n_blocks, dtype=torch.float32, device=device)
    grid = (n_blocks, E)
    num_k = K // BLOCK_K
    print(f"E={E} N={N} K={K} BLOCK_N={BLOCK_N} bytes={nbytes/2**20:.0f} MiB "
          f"programs={n_blocks*E} tile={BLOCK_N*BLOCK_K} B reps={REPS}")
    run(_strided, grid, (w, out, w.stride(0), w.stride(1), num_k, BLOCK_N, BLOCK_K), "strided", nbytes)
    run(_strided2, grid, (w, out, w.stride(0), w.stride(1), num_k, BLOCK_N, BLOCK_K), "strided2", nbytes)
    # Pre-tiled copy: [E, n_blocks, num_k, BLOCK_N * BLOCK_K], read contiguously.
    wt = w.view(E, n_blocks, BLOCK_N, num_k, BLOCK_K).permute(0, 1, 3, 2, 4).contiguous()
    run(_contig, grid, (wt, out, wt.stride(0), BLOCK_N * BLOCK_K, num_k), "contig", nbytes)


if __name__ == "__main__":
    main()
