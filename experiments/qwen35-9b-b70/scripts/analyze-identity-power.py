#!/usr/bin/env python3
"""Compare two identity arms by divergent-request rate, not by per-pass pass/fail.

The two-card c64 identity metric is intermittent: a pass reports n/64, and at a rate near one miss
per 64 requests two passes carry almost no information. Counting divergent requests across many
passes uses every request instead of collapsing 64 of them into one bit, and converges far faster.

Reports each arm's rate with its sample size and a Poisson-style comparison, so "no misses in N
requests" is stated with the N that makes it meaningful rather than as a bare zero.

usage: analyze-identity-power.py CONTROL_ROOT CANDIDATE_ROOT [--lane ladder-mtp0] [--json OUT]
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path


def arm(root: Path, lane: str):
    p = root / lane / "ladder.json"
    if not p.exists():
        return None
    batches = json.loads(p.read_text())["batches"]
    misses = sum(b["oracle_exact_total"] - b["oracle_exact_count"] for b in batches)
    total = sum(b["oracle_exact_total"] for b in batches)
    tps = [b["aggregate_tok_s_wall"] for b in batches]
    return {"passes": len(batches), "requests": total, "divergent": misses,
            "rate_pct": round(100 * misses / total, 4) if total else None,
            "tok_s_mean": round(sum(tps) / len(tps), 1) if tps else None,
            "per_pass": [b["oracle_exact_total"] - b["oracle_exact_count"] for b in batches]}


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    lane = "ladder-mtp0"
    if "--lane" in sys.argv:
        lane = sys.argv[sys.argv.index("--lane") + 1]
    if len(args) < 2:
        print(__doc__)
        return 2
    ctl, cand = arm(Path(args[0]), lane), arm(Path(args[1]), lane)
    if ctl is None or cand is None:
        print(f"missing ladder.json for lane {lane} in one of the arms")
        return 1

    print(f"lane: {lane}")
    for name, a in (("control", ctl), ("candidate", cand)):
        print(f"  {name:10} {a['divergent']:>4} divergent / {a['requests']:>5} requests "
              f"({a['rate_pct']}%) over {a['passes']} passes, {a['tok_s_mean']} tok/s")

    out = {"lane": lane, "control": ctl, "candidate": cand}
    # A zero count is only meaningful against the control rate: if the control rate held, how many
    # would we have expected, and how unlikely is observing none?
    if ctl["divergent"] and cand["requests"]:
        p = ctl["divergent"] / ctl["requests"]
        expected = p * cand["requests"]
        p_none = math.exp(-expected)
        out["expected_if_unchanged"] = round(expected, 2)
        out["p_observing_zero_if_unchanged"] = round(p_none, 5)
        print(f"\n  if the candidate behaved like the control it would show about "
              f"{expected:.1f} divergent requests")
        if cand["divergent"] == 0:
            print(f"  it shows none; probability of that under the control rate is {p_none:.4f}")
            out["verdict"] = ("candidate shows zero divergences where the control rate predicts "
                              f"{expected:.1f}; unlikely under no change (p={p_none:.4f})"
                              if p_none < 0.05 else
                              f"candidate shows zero but the control rate only predicts {expected:.1f}; "
                              "not enough requests to conclude - run more passes")
        else:
            print(f"  it shows {cand['divergent']}; not a removal")
            out["verdict"] = "candidate still diverges; not a fix"
    elif not ctl["divergent"]:
        out["verdict"] = ("the control itself showed no divergences in this run, so the experiment has "
                          "no signal to measure against - the arms cannot be separated")
        print(f"\n  {out['verdict']}")
    print()
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(out, indent=1) + "\n")
        print(f"wrote {sys.argv[sys.argv.index('--json') + 1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
