#!/usr/bin/env python3
"""Can chunking the variance reduction preserve the oracle's values without paying row-at-a-time?

Reformulating the reduction in PyTorch does not remove its shape dependence - sum, matmul and
unsqueeze formulations all track the native mean exactly. But the per-row-count data from that probe
contains a lever: at 2 and 8 rows, zero rows differ from the same row computed alone. The dependence
only appears from 16 rows up.

If that holds, splitting the batch into fixed chunks of C rows and reducing each chunk separately
gives results identical to the M=1 oracle - the property the identity gates actually test - while
costing M/C kernel launches instead of M. At 128 rows with C=8 that is 16 launches against 128.

This measures, for each chunk size: how many rows differ from their own M=1 value, and what a forward
costs. A usable C is one with zero differences and a cost near the unchunked op.
"""
from __future__ import annotations

import json
import os
import time

import torch


def rms_chunked(x, w, eps, chunk):
    orig = x.dtype
    xf = x.to(torch.float32)
    sq = xf.pow(2)
    if chunk is None or x.shape[0] <= chunk:
        var = sq.mean(dim=-1, keepdim=True)
    else:
        var = torch.cat([sq[i:i + chunk].mean(dim=-1, keepdim=True)
                         for i in range(0, sq.shape[0], chunk)], 0)
    xf = xf * torch.rsqrt(var + eps)
    if w is not None:
        xf = xf.to(w.dtype) * w
    return xf.to(orig)


def main() -> int:
    dev, dtype, eps = "xpu", torch.float16, 1e-6
    hidden = int(os.environ.get("HIDDEN", "4096"))
    rows_list = [int(x) for x in os.environ.get("ROWS", "16,32,64,128").split(",")]
    seeds = [int(x) for x in os.environ.get("SEEDS", "0,1,2,3,4,5,6,7").split(",")]
    chunks = [int(x) for x in os.environ.get("CHUNKS", "1,2,4,8,16,32").split(",")] + [None]

    from vllm.config import VllmConfig, set_current_vllm_config
    from vllm.model_executor.layers.layernorm import RMSNorm
    with set_current_vllm_config(VllmConfig()):
        norm = RMSNorm(hidden, eps=eps).to(dev).to(dtype)
    torch.manual_seed(0)
    with torch.no_grad():
        norm.weight.copy_(torch.randn(hidden, device=dev, dtype=dtype) * 0.02 + 1.0)
    w = norm.weight.data

    report = {"hidden": hidden, "seeds": len(seeds), "chunks": {}}
    print(f"hidden={hidden} seeds={len(seeds)} rows={rows_list}\n")
    print(f"{'chunk':>7} {'rows differing from native M=1':>32} {'us/forward @128':>17}")
    for c in chunks:
        diff = total = 0
        per = {}
        for m in rows_list:
            d = 0
            for sd in seeds:
                torch.manual_seed(sd)
                x = torch.randn(m, hidden, device=dev, dtype=dtype)
                with torch.no_grad():
                    batched = rms_chunked(x, w, eps, c)
                    oracle = [norm(x[i:i + 1].clone())[0] for i in range(m)]
                torch.xpu.synchronize()
                d += sum(1 for i, o in enumerate(oracle)
                         if not torch.equal(batched[i].view(torch.int16), o.view(torch.int16)))
            per[m] = d; diff += d; total += m * len(seeds)
        torch.manual_seed(0)
        x = torch.randn(128, hidden, device=dev, dtype=dtype)
        with torch.no_grad():
            for _ in range(5):
                rms_chunked(x, w, eps, c)
            torch.xpu.synchronize()
            t0 = time.perf_counter()
            for _ in range(50):
                rms_chunked(x, w, eps, c)
            torch.xpu.synchronize()
            us = (time.perf_counter() - t0) / 50 * 1e6
        label = "none" if c is None else str(c)
        print(f"{label:>7} {diff:>10}/{total:<10} {str(per):>18} {us:>10.1f}")
        report["chunks"][label] = {"differing_vs_native_m1": diff, "rows_compared": total,
                                   "per_row_count": per, "us_per_forward_128": round(us, 1),
                                   "matches_oracle": diff == 0}
    good = [k for k, v in report["chunks"].items() if v["matches_oracle"]]
    print(f"\nchunk sizes whose every row equals the native M=1 oracle: {good or 'none'}")
    report["oracle_preserving_chunks"] = good
    out = os.environ.get("OUT")
    if out:
        with open(out, "w") as f:
            json.dump(report, f, indent=1)
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
