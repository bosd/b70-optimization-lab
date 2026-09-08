#!/usr/bin/env python3
"""What does QSA's stable argsort selection cost at the benchmark's decode shapes?

The XPU path selects indexer blocks with a full stable argsort and then slices:

    ranked = torch.argsort(logits, dim=1, descending=True, stable=True)[:, :block_topk]

chosen because the generic XPU top-k resolves ties by atomic reservation order, so both
the order and the selected set can vary between launches, and QSA consumes the order
directly. The order is therefore load-bearing for exactness and cannot simply be dropped.

What can be asked is how much the sort costs, and whether a cheaper kernel producing the
same score-desc / logical-index-asc order would be worth building. With indexer_budget
2048 and compress_ratio 4: at a 2048-token context 512 blocks are visible and all 512 are
kept, so the sort buys ordering only; at 4096, 1024 are visible and 512 kept.

This times the op itself against two references at those shapes -- it does not rank kernel
variants, which on this machine has to be done in the server (A320/A327).

  PYTHONPATH=<stage>:<overlay> ... probe-qsa-selection-argsort-offline.py
"""
import os
import time

import torch

device = torch.device("xpu:0")
torch.xpu.set_device(device)
LAYERS = int(os.getenv("Q38_PROBE_LAYERS", "48"))
REPS = int(os.getenv("Q38_PROBE_REPS", "50"))


def bench(fn, *args):
    for _ in range(5):
        fn(*args)
    torch.xpu.synchronize()
    t0 = time.perf_counter()
    for _ in range(REPS):
        fn(*args)
    torch.xpu.synchronize()
    return (time.perf_counter() - t0) / REPS


def main() -> None:
    g = torch.Generator(device=device).manual_seed(5)
    print(f"per-call microseconds, and the cost of {LAYERS} layers of it")
    print(f"{'rows':>5} {'cols':>6} {'k':>5} {'argsort(stable)':>16} {'topk(sorted)':>13} {'sort values':>12}   {'x48 argsort':>12}")
    for rows in (1, 4):
        for cols, k in ((512, 512), (1024, 512), (2048, 512)):
            logits = torch.randn(rows, cols, generator=g, device=device)
            t_arg = bench(lambda x: torch.argsort(x, dim=1, descending=True, stable=True)[:, :k], logits)
            t_topk = bench(lambda x: torch.topk(x, k, dim=1, sorted=True), logits)
            t_sortv = bench(lambda x: torch.sort(x, dim=1, descending=True), logits)
            print(f"{rows:5d} {cols:6d} {k:5d} {t_arg*1e6:16.1f} {t_topk*1e6:13.1f} {t_sortv*1e6:12.1f}   {t_arg*LAYERS*1e3:11.3f} ms")


if __name__ == "__main__":
    main()
