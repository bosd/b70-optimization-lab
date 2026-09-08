#!/usr/bin/env python3
"""Difference two routing-census snapshots into the routing of the window between them.

The census counters are cumulative from process start, so a single dump mixes the startup
profiling run's dummy-input routing with everything after it. Two SIGUSR1 snapshots taken
around a generation bracket that generation, and their difference is its routing alone —
which is what the placement builder should see, since the placement only has to avoid the
experts a decode window selects.

Emits the same shape the census hook writes, so
`build-q38-expert-host-placement-from-census.py` consumes it unchanged.

  diff-q38-placement-census-snapshots.py --before <snap01-rank0.json> --after <snap02-rank0.json> \
      --out <window-rank0.json>
"""
from __future__ import annotations

import argparse
import json


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    before = json.load(open(a.before))
    after = json.load(open(a.after))
    out: dict[str, dict] = {}
    total = negative = 0
    for layer, entry in after.items():
        prev = before.get(layer, {}).get("counts", {})
        counts = {}
        for e, n in entry.get("counts", {}).items():
            d = int(n) - int(prev.get(e, 0))
            if d < 0:
                negative += 1
                continue
            if d:
                counts[e] = d
                total += d
        out[layer] = {"counts": counts, "host": entry.get("host", [])}
    if negative:
        raise SystemExit(f"{negative} counts went backwards between snapshots: not the same process")
    hosts = sum(len(v["host"]) for v in out.values())
    print(f"{a.out}: {total} routed selections in the window across {len(out)} layers, "
          f"{sum(len(v['counts']) for v in out.values())} distinct (layer, expert) pairs selected, "
          f"{hosts} parked")
    json.dump(out, open(a.out, "w"))


if __name__ == "__main__":
    main()
