#!/usr/bin/env python3
"""Which RMSNorm implementations are row-count invariant, and what do they cost?

The norm on Qwen3.5's serving path is not row-count invariant: about 2-3% of rows differ from the
same row computed alone once the batch reaches 16, which is the residue the row-wise all-reduce
experiment could not remove. This asks the next question - whether any implementation of the same
maths does have the property, since a fix has to exist before it can be measured end to end.

Candidates, all computing the same function:
  native      the op the server runs today (ir.ops.rms_norm), as a control that must fail
  torch_fp16  the textbook expression in the serving dtype
  torch_fp32  the same expression with the reduction accumulated in float32
  rowwise     each row normalised alone, invariant by construction, as the slow upper bound

For each: how many rows differ from that row computed alone, and how long a forward takes. A
candidate is only interesting if it is invariant AND cheap; rowwise establishes what "correct but
unusable" costs.
"""
from __future__ import annotations

import json
import os
import time

import torch


def rms_native(norm, x):
    return norm(x.clone())


def rms_torch(x, weight, eps, acc_dtype):
    xa = x.to(acc_dtype)
    var = xa.pow(2).mean(-1, keepdim=True)
    out = xa * torch.rsqrt(var + eps)
    return (out * weight.to(acc_dtype)).to(x.dtype)


def differing_rows(batched, singles):
    n = 0
    for i, s in enumerate(singles):
        if not torch.equal(batched[i].view(torch.int16), s.view(torch.int16)):
            n += 1
    return n


def main() -> int:
    dev, dtype = "xpu", torch.float16
    hidden = int(os.environ.get("HIDDEN", "4096"))
    rows_list = [int(x) for x in os.environ.get("ROWS", "16,32,64,128").split(",")]
    seeds = [int(x) for x in os.environ.get("SEEDS", "0,1,2,3,4").split(",")]
    eps = 1e-6

    from vllm.config import VllmConfig, set_current_vllm_config
    from vllm.model_executor.layers.layernorm import RMSNorm

    with set_current_vllm_config(VllmConfig()):
        norm = RMSNorm(hidden, eps=eps).to(dev).to(dtype)
    torch.manual_seed(0)
    with torch.no_grad():
        norm.weight.copy_(torch.randn(hidden, device=dev, dtype=dtype) * 0.02 + 1.0)
    weight = norm.weight.data

    variants = {
        "native": lambda x: rms_native(norm, x),
        "torch_fp16": lambda x: rms_torch(x, weight, eps, torch.float16),
        "torch_fp32": lambda x: rms_torch(x, weight, eps, torch.float32),
        "rowwise": lambda x: torch.cat([rms_torch(x[i:i + 1], weight, eps, torch.float32)
                                        for i in range(x.shape[0])], 0),
    }

    report = {"hidden": hidden, "dtype": str(dtype), "seeds": len(seeds), "variants": {}}
    print(f"hidden={hidden} dtype={dtype} seeds={len(seeds)}\n")
    print(f"{'variant':12} {'rows':>5} {'differing':>12} {'rate':>8} {'us/forward':>11}")
    for name, fn in variants.items():
        entry = {"rows": {}}
        for m in rows_list:
            diff = total = 0
            for sd in seeds:
                torch.manual_seed(sd)
                x = torch.randn(m, hidden, device=dev, dtype=dtype)
                with torch.no_grad():
                    batched = fn(x)
                    singles = [fn(x[i:i + 1])[0] for i in range(m)]
                torch.xpu.synchronize()
                diff += differing_rows(batched, singles)
                total += m
            # timing on the largest seed's shape, after a warmup
            torch.manual_seed(0)
            x = torch.randn(m, hidden, device=dev, dtype=dtype)
            with torch.no_grad():
                for _ in range(5):
                    fn(x)
                torch.xpu.synchronize()
                t0 = time.perf_counter()
                for _ in range(50):
                    fn(x)
                torch.xpu.synchronize()
                us = (time.perf_counter() - t0) / 50 * 1e6
            rate = 100.0 * diff / total
            print(f"{name:12} {m:>5} {diff:>5}/{total:<6} {rate:>7.2f}% {us:>10.1f}")
            entry["rows"][m] = {"differing": diff, "compared": total, "rate_pct": round(rate, 3),
                                "us_per_forward": round(us, 1)}
        entry["invariant"] = all(v["differing"] == 0 for v in entry["rows"].values())
        report["variants"][name] = entry
        print()

    out = os.environ.get("OUT")
    if out:
        with open(out, "w") as f:
            json.dump(report, f, indent=1)
        print(f"wrote {out}")
    inv = [n for n, e in report["variants"].items() if e["invariant"]]
    print(f"row-count invariant in this sample: {inv or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
