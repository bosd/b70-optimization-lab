#!/usr/bin/env python3
"""Is the FP16 vocabulary projection row-count invariant?

The lab's fixed-K work made the weight-quantised projections invariant to how many decode rows share
a step, and its predicate is `(Ta_ext == u4 || s4) && Tb_ext == f16` - weight-quantised only. On this
route the target verifier's lm_head is plain FP16 by design (only the draft head is INT4), so it sits
outside that coverage. It is also the last matmul before the argmax, which is where a tie is actually
decided, so a row-count dependence there would flip tokens directly.

Same method as the RMSNorm probe: the same rows alone and batched, compared bitwise, no server and no
second card. Also reports whether any difference is large enough to move an argmax, since a last-bit
logit change only matters when it lands on a near-tie.
"""
from __future__ import annotations

import json
import os

import torch


def main() -> int:
    dev, dtype = "xpu", torch.float16
    hidden = int(os.environ.get("HIDDEN", "4096"))
    vocab = int(os.environ.get("VOCAB", "248320"))
    rows_list = [int(x) for x in os.environ.get("ROWS", "2,4,8,16,32,64").split(",")]
    seeds = [int(x) for x in os.environ.get("SEEDS", "0,1,2").split(",")]

    torch.manual_seed(0)
    w = (torch.randn(vocab, hidden, device=dev, dtype=dtype) * 0.02)
    report = {"hidden": hidden, "vocab": vocab, "dtype": str(dtype), "seeds": len(seeds), "rows": {}}
    print(f"lm_head shape [M, {hidden}] x [{hidden}, {vocab}] in {dtype}, {len(seeds)} seed(s)\n")
    print(f"{'rows':>5} {'differing rows':>16} {'max |dlogit|':>13} {'argmax changed':>15}")
    for m in rows_list:
        diff = total = argmax_changed = 0
        maxd = 0.0
        for sd in seeds:
            torch.manual_seed(sd)
            x = torch.randn(m, hidden, device=dev, dtype=dtype)
            with torch.no_grad():
                batched = torch.nn.functional.linear(x, w)
                singles = [torch.nn.functional.linear(x[i:i + 1], w)[0] for i in range(m)]
            torch.xpu.synchronize()
            for i, s in enumerate(singles):
                b = batched[i]
                if not torch.equal(b.view(torch.int16), s.view(torch.int16)):
                    diff += 1
                    maxd = max(maxd, float((b.float() - s.float()).abs().max()))
                    if int(b.argmax()) != int(s.argmax()):
                        argmax_changed += 1
                total += 1
        rate = 100.0 * diff / total
        print(f"{m:>5} {diff:>6}/{total:<8} {rate:>5.1f}% {maxd:>12.3e} {argmax_changed:>10}/{diff or 1}")
        report["rows"][m] = {"differing": diff, "compared": total, "rate_pct": round(rate, 2),
                            "max_abs_logit_delta": maxd, "argmax_changed": argmax_changed}
    any_diff = any(v["differing"] for v in report["rows"].values())
    any_argmax = any(v["argmax_changed"] for v in report["rows"].values())
    print(f"\nverdict: lm_head GEMM is {'ROW-COUNT DEPENDENT' if any_diff else 'row-count invariant'}"
          f"; argmax {'moved' if any_argmax else 'never moved'} in this sample")
    out = os.environ.get("OUT")
    if out:
        with open(out, "w") as f:
            json.dump(report, f, indent=1)
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
