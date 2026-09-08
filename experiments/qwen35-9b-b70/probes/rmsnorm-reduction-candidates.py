#!/usr/bin/env python3
"""Find a variance reduction that is row-count invariant AND agrees with the native op at M=1.

The native RMSNorm is pure PyTorch - no custom kernel - so its shape dependence lives in
`x.pow(2).mean(dim=-1)` on a float32 tensor, and a fix needs no oneDNN rebuild.

The target is specific. Exactly preserving native's output at every row count is impossible: native
already disagrees with itself across row counts, which is the bug. But the identity gates compare a
batch against a sequential oracle, and that oracle runs one row at a time. So a replacement that is

  (a) row-count invariant, and
  (b) bit-identical to native at M=1

makes every batch reproduce the published oracle exactly. That preserves every recorded oracle output
and would close the ladders without re-qualifying the lane, which a merely-invariant variant cannot.

Candidates keep native's structure otherwise (float32 variance, cast to weight dtype before the
weight multiply) and vary only how the sum over the hidden dimension is formed.
"""
from __future__ import annotations

import json
import os

import torch


def make_variants(hidden: int):
    ones = None

    def mean_native(x2):
        return x2.mean(dim=-1, keepdim=True)

    def mean_sum_div(x2):
        return x2.sum(dim=-1, keepdim=True) / x2.shape[-1]

    def mean_matmul(x2):
        nonlocal ones
        if ones is None or ones.device != x2.device:
            ones = torch.ones(x2.shape[-1], 1, device=x2.device, dtype=torch.float32)
        return (x2 @ ones) / x2.shape[-1]

    def mean_unsqueeze(x2):
        # Reduce each row as its own 1-D problem by folding the row index into a leading batch dim
        # of size 1; the reduction sees the same shape whatever M is.
        return x2.unsqueeze(1).sum(dim=-1, keepdim=True).squeeze(1) / x2.shape[-1]

    return {"native_mean": mean_native, "sum_div": mean_sum_div,
            "matmul_ones": mean_matmul, "unsqueeze_sum": mean_unsqueeze}


def rms(x, weight, eps, mean_fn):
    orig = x.dtype
    xf = x.to(torch.float32)
    var = mean_fn(xf.pow(2))
    xf = xf * torch.rsqrt(var + eps)
    if weight is not None:
        xf = xf.to(weight.dtype) * weight
    return xf.to(orig)


def main() -> int:
    dev, dtype, eps = "xpu", torch.float16, 1e-6
    hidden = int(os.environ.get("HIDDEN", "4096"))
    rows_list = [int(x) for x in os.environ.get("ROWS", "2,8,16,32,64,128").split(",")]
    seeds = [int(x) for x in os.environ.get("SEEDS", "0,1,2,3,4").split(",")]

    from vllm.config import VllmConfig, set_current_vllm_config
    from vllm.model_executor.layers.layernorm import RMSNorm
    with set_current_vllm_config(VllmConfig()):
        norm = RMSNorm(hidden, eps=eps).to(dev).to(dtype)
    torch.manual_seed(0)
    with torch.no_grad():
        norm.weight.copy_(torch.randn(hidden, device=dev, dtype=dtype) * 0.02 + 1.0)
    w = norm.weight.data
    variants = make_variants(hidden)

    report = {"hidden": hidden, "seeds": len(seeds), "candidates": {}}
    print(f"hidden={hidden} seeds={len(seeds)}\n")
    print(f"{'candidate':15} {'matches native @M=1':>20} {'differing rows (batched vs own M=1)':>38}")
    for name, fn in variants.items():
        # (b) agreement with the native op at one row
        m1_exact = m1_total = 0
        for sd in seeds:
            torch.manual_seed(sd)
            x = torch.randn(1, hidden, device=dev, dtype=dtype)
            with torch.no_grad():
                a = norm(x.clone())
                b = rms(x, w, eps, fn)
            torch.xpu.synchronize()
            m1_exact += int(torch.equal(a.view(torch.int16), b.view(torch.int16))); m1_total += 1
        # (a) row-count invariance of the candidate against itself at M=1
        diff = total = 0
        per_rows = {}
        for m in rows_list:
            d = 0
            for sd in seeds:
                torch.manual_seed(sd)
                x = torch.randn(m, hidden, device=dev, dtype=dtype)
                with torch.no_grad():
                    batched = rms(x, w, eps, fn)
                    singles = [rms(x[i:i + 1], w, eps, fn)[0] for i in range(m)]
                torch.xpu.synchronize()
                d += sum(1 for i, s in enumerate(singles)
                         if not torch.equal(batched[i].view(torch.int16), s.view(torch.int16)))
            per_rows[m] = d
            diff += d; total += m * len(seeds)
        ok = "yes" if m1_exact == m1_total else f"{m1_exact}/{m1_total}"
        print(f"{name:15} {ok:>20} {diff:>12}/{total:<8} {per_rows}")
        report["candidates"][name] = {"matches_native_at_m1": m1_exact == m1_total,
                                      "m1_exact": m1_exact, "m1_total": m1_total,
                                      "differing_rows": diff, "rows_compared": total,
                                      "per_row_count": per_rows,
                                      "invariant": diff == 0}
    winners = [n for n, c in report["candidates"].items()
               if c["invariant"] and c["matches_native_at_m1"]]
    print(f"\ninvariant AND native-equal at M=1: {winners or 'none'}")
    report["winners"] = winners
    out = os.environ.get("OUT")
    if out:
        with open(out, "w") as f:
            json.dump(report, f, indent=1)
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
