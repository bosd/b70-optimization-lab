#!/usr/bin/env python3
"""Is the RMSNorm's result for a row independent of how many rows share the batch?

The two-card identity loss is not explained by the cross-card all-reduce alone (campaign r0/r1). The
Flash-Next lane's precedent says to look for a second shape-dependent reduction, and there it was a
norm: its mean was reduced in a shape-dependent order, so a two-row batch differed from the same
rows alone. This asks the same question of the norm Qwen3.5 actually runs here.

No server and no second card: the op is instantiated directly and fed the same rows alone and in a
batch. If a row's output changes with the batch it shares, that is a row-count dependence in the
norm, which would produce exactly the residue the all-reduce experiment could not remove.

The probe carries its own control: if it were simply measuring noise it would report differences at
every row count. A clean threshold - invariant below some M, dependent above - is the signature of a
shape-dependent reduction rather than a broken comparison, and is what the run below reports.
"""
from __future__ import annotations

import json
import os
import sys

import torch


def bitwise_differing_rows(batched: torch.Tensor, singles: list[torch.Tensor]) -> int:
    diff = 0
    for i, single in enumerate(singles):
        a = batched[i].view(torch.int16 if batched.dtype == torch.float16 else torch.int32)
        b = single[0].view(torch.int16 if single.dtype == torch.float16 else torch.int32)
        if not torch.equal(a, b):
            diff += 1
    return diff


def first_differing_element(batched: torch.Tensor, singles: list[torch.Tensor]):
    for i, single in enumerate(singles):
        neq = (batched[i] != single[0]).nonzero()
        if neq.numel():
            j = int(neq[0])
            return i, j, float(batched[i][j]), float(single[0][j])
    return None


def main() -> int:
    dev = "xpu"
    dtype = torch.float16
    hidden = int(os.environ.get("HIDDEN", "4096"))     # Qwen3.5-9B hidden size
    rows_list = [int(x) for x in os.environ.get("ROWS", "2,4,8,16,32,64,96,128").split(",")]
    torch.manual_seed(int(os.environ.get('SEED', '0')))

    from vllm.config import VllmConfig, set_current_vllm_config
    from vllm.model_executor.layers.layernorm import RMSNorm

    # RMSNorm is a CustomOp: it picks its forward implementation from the active vLLM config at
    # construction time, so it has to be built inside one or it dispatches nothing.
    with set_current_vllm_config(VllmConfig()):
        norm = RMSNorm(hidden, eps=1e-6).to(dev).to(dtype)
    with torch.no_grad():
        norm.weight.copy_(torch.randn(hidden, device=dev, dtype=dtype) * 0.02 + 1.0)
    bound = getattr(norm, "_forward_method", None)
    bound_name = getattr(bound, "__name__", str(bound))
    print(f"dispatched forward: {bound_name}")

    report = {"device": str(dev), "dtype": str(dtype), "hidden": hidden, "seed": int(os.environ.get("SEED","0")),
              "vllm_xpu_rmsnorm_triton": os.environ.get("VLLM_XPU_RMSNORM_TRITON"),
              "dispatched_forward": bound_name,
              "results": []}

    seeds = [int(x) for x in os.environ.get("SEEDS", os.environ.get("SEED", "0")).split(",")]
    print(f"RMSNorm row-invariance, hidden={hidden}, dtype={dtype}, {len(seeds)} seed(s)")
    print(f"{'rows':>6} {'differing rows':>16} {'rate':>9}   example difference")
    for m in rows_list:
        total_diff = 0
        example = None
        for sd in seeds:
            torch.manual_seed(sd)
            x = torch.randn(m, hidden, device=dev, dtype=dtype)
            with torch.no_grad():
                batched = norm(x.clone())
                singles = [norm(x[i:i + 1].clone()) for i in range(m)]
            torch.xpu.synchronize()
            total_diff += bitwise_differing_rows(batched, singles)
            if example is None:
                fd = first_differing_element(batched, singles)
                if fd is not None:
                    example = fd
        denom = m * len(seeds)
        rate = 100.0 * total_diff / denom
        note = "-" if example is None else f"elem {example[1]}: {example[2]!r} vs {example[3]!r}"
        print(f"{m:>6} {total_diff:>7}/{denom:<8} {rate:>7.2f}%   {note}")
        report["results"].append({"rows": m, "seeds": len(seeds), "differing_rows": total_diff,
                                  "rows_compared": denom, "rate_pct": round(rate, 3),
                                  "example": None if example is None else
                                  {"element": example[1], "batched": example[2], "alone": example[3]}})

    out = os.environ.get("OUT")
    if out:
        with open(out, "w") as f:
            json.dump(report, f, indent=1)
        print(f"\nwrote {out}")
    any_diff = any(r["differing_rows"] for r in report["results"])
    print(f"\nverdict: RMSNorm is {'ROW-COUNT DEPENDENT' if any_diff else 'row-count invariant'} on this path")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
