#!/usr/bin/env python3
"""Tabulate strict-stage campaigns: throughput per server and the four identity gates.

Reads campaign roots under /mnt/fast-ai/bench-results and prints one row per campaign, so a depth
sweep or an image comparison can be read without opening each campaign.log. Speed alone is not the
verdict for this lab: a candidate that is faster but scores under 12/12 on G3 is not lossless, which
is how depths 4-6 were withheld on the FP8 route.

usage: summarize-strict-campaigns.py ROOT [ROOT ...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

GATE_RE = re.compile(r"(G[123][^:]*): (\d+/\d+)")
PERF_RE = re.compile(r"(\S+): class_balanced_median_tok_s=([0-9.]+)")


def main() -> int:
    roots = [Path(a) for a in sys.argv[1:]]
    if not roots:
        print(__doc__)
        return 2
    print(f"{'campaign':52} {'config':30} {'server medians (tok/s)':38} gates")
    for root in roots:
        log = root / "campaign.log"
        if not log.exists():
            print(f"{root.name:52} (no campaign.log)")
            continue
        text = log.read_text()
        cfg = (root / "config.txt").read_text().strip() if (root / "config.txt").exists() else ""
        cfg_short = " ".join(p for p in cfg.split() if p.split("=")[0] in
                             {"RUN", "TP", "DEPTH", "GRAPH", "DRAFT_HEAD", "PAD"})
        perf = PERF_RE.findall(text)
        gates = GATE_RE.findall(text)
        speeds = "  ".join(f"{lbl}={float(v):.2f}" for lbl, v in perf if lbl.startswith("mtp") and not lbl.startswith("mtp0"))
        oracle = "  ".join(f"{lbl}={float(v):.2f}" for lbl, v in perf if lbl.startswith("mtp0"))
        gate_s = " ".join(f"{g.split()[0]}:{v}" for g, v in gates)
        lossless = all(v.split("/")[0] == v.split("/")[1] for _, v in gates) if gates else None
        mark = "lossless" if lossless else ("NOT LOSSLESS" if gates else "no gates")
        print(f"{root.name:52} {cfg_short:30} {speeds:38} {gate_s}  -> {mark}")
        if oracle:
            print(f"{'':52} {'oracle:':30} {oracle}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
