#!/usr/bin/env python3
"""Is the INT4 W4A16 body GEMM actually row-count invariant at this model's shapes?

Everything in this line of work has assumed it is. That assumption is what makes the INT4 route the
"exact" one, and it rests on the oneDNN fixed-K two-tier patch, whose screening was done on the
Qwen3.8-27B lane's shapes. Qwen3.5-9B has different projections, and on two cards they are sharded
again. If the invariance does not hold at some row count on these shapes, that is the answer to the
whole question - and nobody has checked.

Probes torch.ops._xpu_C.int4_gemm_w4a16 directly at the 9B's four projection shapes, TP1 and the TP2
shard, the same way the norm and the vocabulary projection were probed: the same rows alone and
batched, compared bitwise.

STATUS: incomplete. The op schema is
`(Tensor A, Tensor B, Tensor? bias, Tensor B_scale, Tensor B_zp, int group_size, Tensor? g_idx)`,
recovered from the registered JIT schema, but synthetic packed weights are rejected with "could not
construct a memory descriptor using strides" - the packed layout oneDNN expects is not reproduced by
the obvious `[K, N//2]` uint8 / `[K//group, N]` scale shapes used here. Finishing this means taking
the layout from a loaded checkpoint rather than synthesising it.

Weigh that against the fact that the invariance is already screened: R220/R221 report the two-tier
selection bitwise equal on all 14 TP1 and TP2 shapes for n = 1..1024, which is why the GEMM was
eliminated as a suspect by reading the patch rather than by running this. Finish it only if that
screening is doubted.
"""
from __future__ import annotations

import json
import os

import torch


def main() -> int:
    dev, dtype = "xpu", torch.float16
    group = 128
    rows_list = [int(x) for x in os.environ.get("ROWS", "2,8,16,32,33,48,64,96,128").split(",")]
    seeds = [int(x) for x in os.environ.get("SEEDS", "0,1").split(",")]
    # (name, out_features, in_features) for Qwen3.5-9B; TP2 halves the sharded dimension.
    shapes = [("qkv", 6144, 4096), ("o", 4096, 4096), ("gate_up", 24576, 4096), ("down", 4096, 12288)]
    if os.environ.get("TP") == "2":
        shapes = [("qkv/2", 3072, 4096), ("o", 4096, 2048), ("gate_up/2", 12288, 4096), ("down", 4096, 6144)]

    import vllm._xpu_ops  # registers the _xpu_C op namespace  # noqa: F401

    op = torch.ops._xpu_C.int4_gemm_w4a16
    report = {"dtype": str(dtype), "group_size": group, "tp": os.environ.get("TP", "1"), "shapes": {}}
    print(f"int4_gemm_w4a16, group {group}, TP{report['tp']}, {len(seeds)} seed(s)\n")
    print(f"{'shape':>12} {'N':>6} {'K':>6} {'rows':>5} {'differing':>12}")
    for name, N, K in shapes:
        torch.manual_seed(0)
        qw = torch.randint(0, 255, (K, N // 2), device=dev, dtype=torch.uint8)
        # schema: (A, B, bias?, B_scale, B_zp, group_size, g_idx?)
        scales = (torch.rand(K // group, N, device=dev, dtype=dtype) * 0.02 + 0.01)
        zp = torch.zeros(K // group, N // 2, device=dev, dtype=torch.uint8)
        entry = {}
        for m in rows_list:
            diff = total = 0
            for sd in seeds:
                torch.manual_seed(sd)
                x = torch.randn(m, K, device=dev, dtype=dtype)
                try:
                    with torch.no_grad():
                        batched = op(x, qw, None, scales, zp, group, None)
                        singles = [op(x[i:i + 1], qw, None, scales, zp, group, None)[0] for i in range(m)]
                except Exception as exc:  # signature differs from the guess
                    print(f"  op call failed: {type(exc).__name__}: {str(exc)[:140]}")
                    return 1
                torch.xpu.synchronize()
                for i, s in enumerate(singles):
                    if not torch.equal(batched[i].view(torch.int16), s.view(torch.int16)):
                        diff += 1
                    total += 1
            print(f"{name:>12} {N:>6} {K:>6} {m:>5} {diff:>5}/{total:<6} {'' if diff==0 else '  <-- ROW DEPENDENT'}")
            entry[m] = {"differing": diff, "compared": total}
        report["shapes"][name] = entry
    any_diff = any(v["differing"] for e in report["shapes"].values() for v in e.values())
    print(f"\nverdict: W4A16 body GEMM is {'ROW-COUNT DEPENDENT' if any_diff else 'row-count invariant'} "
          f"at these shapes")
    out = os.environ.get("OUT")
    if out:
        with open(out, "w") as f:
            json.dump(report, f, indent=1)
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
