#!/usr/bin/env python3
"""Summarise the Gemma 4 26B Q8 replay distribution and draft-thread sweep on this host.

The recipe currently says the 2026-09-07 replays land "within the known several-percent spread"
under the 124.977 record. Three runs cannot separate a wide tail from a systematic difference, and
the lane's own documented repeatability is a 2.324% run-median CV with a 4.409% p90 pairwise delta,
which the observed shortfall exceeds. This reports what the samples actually support.

usage: analyze-20260907-replay-distribution.py [--json OUT]
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECORD = 124.97714084813418
METRIC = "tok_s_1_100_after_ttft"

GROUPS = {
    "record settings (32 draft threads)": ["gemma4-q8-gpu0-125repro-container2026.0-*", "gemma4-q8-gpu0-distrib32-*"],
    "16 draft threads": ["gemma4-q8-gpu0-threads16-*"],
    "8 draft threads": ["gemma4-q8-gpu0-threads08-*"],
    "host compatibility build (32 threads)": ["gemma4-q8-gpu0-125repro-compat2026.1-*"],
}


def samples(patterns: list[str]) -> list[tuple[str, float, float, bool]]:
    out = []
    for pat in patterns:
        for d in sorted((ROOT / "data").glob(pat)):
            f = d / "summary.json"
            if not f.exists():
                continue
            s = json.loads(f.read_text())
            b = s.get("bench_summary") or {}
            if METRIC not in b:
                continue
            gate = bool((s.get("realistic_final_gate") or {}).get("passed"))
            out.append((d.name, b[METRIC]["median"],
                        b["class_balanced_tok_s_1_100_intervals_after_ttft"]["median"], gate))
    return out


def main() -> int:
    report = {"record_tok_s": RECORD, "metric": METRIC, "groups": {}}
    for label, pats in GROUPS.items():
        rows = samples(pats)
        if not rows:
            continue
        vals = [v for _, v, _, _ in rows]
        entry = {
            "n": len(vals),
            "median": round(statistics.median(vals), 3),
            "mean": round(statistics.fmean(vals), 3),
            "min": round(min(vals), 3),
            "max": round(max(vals), 3),
            "stdev": round(statistics.stdev(vals), 3) if len(vals) > 1 else None,
            "cv_pct": round(100 * statistics.stdev(vals) / statistics.fmean(vals), 3) if len(vals) > 1 else None,
            "pct_of_record": round(100 * statistics.fmean(vals) / RECORD, 2),
            "all_gates_passed": all(g for _, _, _, g in rows),
            "runs": [{"run": n, "median_tok_s": round(v, 3), "class_balanced": round(c, 3), "gate": g}
                     for n, v, c, g in rows],
        }
        report["groups"][label] = entry
        print(f"== {label}")
        print(f"   n={entry['n']}  median={entry['median']}  mean={entry['mean']}  "
              f"range {entry['min']}-{entry['max']}  cv={entry['cv_pct']}%  "
              f"{entry['pct_of_record']}% of the record  gates={'all pass' if entry['all_gates_passed'] else 'A GATE FAILED'}")

    base = report["groups"].get("record settings (32 draft threads)")
    if base and base["n"] >= 4:
        gap = 100 * (RECORD - base["mean"]) / RECORD
        print(f"\nshortfall against the record: {gap:.2f}% of the record, on {base['n']} samples "
              f"with a {base['cv_pct']}% coefficient of variation")
        if base["max"] < RECORD and base["cv_pct"] is not None:
            spread = (base["max"] - base["min"]) / base["mean"] * 100
            print(f"observed spread here is {spread:.2f}%; the record sits {100*(RECORD-base['max'])/RECORD:.2f}% "
                  f"above the best of these runs")
    for label in ("16 draft threads", "8 draft threads"):
        g = report["groups"].get(label)
        if g and base:
            delta = 100 * (g["mean"] - base["mean"]) / base["mean"]
            print(f"{label}: {delta:+.2f}% vs 32 threads (mean of {g['n']} vs {base['n']})")

    if "--json" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--json") + 1])
        out.write_text(json.dumps(report, indent=1) + "\n")
        print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
