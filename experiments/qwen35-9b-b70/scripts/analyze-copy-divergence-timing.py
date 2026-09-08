#!/usr/bin/env python3
"""Do disagreeing copies of one prompt sit in the same decode step, or drift apart?

Byte-identical prompts issued together sometimes return different completions. Two explanations fit:
the copies occupy different rows of the same step and the result depends on row position, or the
scheduler drifted them into different steps whose compositions differ, which would be batch-shape
dependence again.

The ladder records each request's start time and a per-token offset, so absolute per-token arrival
times are recoverable. Copies executing in the same step must be emitting token N at nearly the same
instant; copies a step apart cannot be. Comparing the spread at the divergence index against the
spread among copies that agree separates the two explanations without new runs.

usage: analyze-copy-divergence-timing.py ROOT [ROOT ...] [--lane ladder-mtp0] [--json OUT]
"""
from __future__ import annotations

import collections
import json
import statistics
import sys
from pathlib import Path


def abs_times(row):
    start = row.get("request_started_epoch_s")
    offs = row.get("token_id_offsets_s") or []
    if start is None:
        return []
    return [start + o for o in offs]


def analyse(root: Path, lane: str):
    d = json.loads((root / lane / "ladder.json").read_text())
    dis, agr = [], []
    slot_of_minority = collections.Counter()
    for b in d["batches"]:
        groups = collections.defaultdict(list)
        for r in b["rows"]:
            groups[r["prompt_sha256"]].append(r)
        for rows in groups.values():
            if len(rows) < 2:
                continue
            outs = collections.Counter(tuple(r.get("token_ids") or []) for r in rows)
            times = {id(r): abs_times(r) for r in rows}
            n = min((len(t) for t in times.values() if t), default=0)
            if n == 0:
                continue
            if len(outs) == 1:
                # spread among copies that agree, at a comparable index
                idx = min(90, n - 1)
                vals = [times[id(r)][idx] for r in rows if len(times[id(r)]) > idx]
                if len(vals) > 1:
                    agr.append(max(vals) - min(vals))
                continue
            # divergence index: first token where the copies are not unanimous
            seqs = [r.get("token_ids") or [] for r in rows]
            k = 0
            while k < n and len({s[k] for s in seqs}) == 1:
                k += 1
            vals = [times[id(r)][k] for r in rows if len(times[id(r)]) > k]
            if len(vals) > 1:
                dis.append({"index": k, "spread_s": max(vals) - min(vals),
                            "copies": len(rows), "distinct_outputs": len(outs)})
            majority, _ = outs.most_common(1)[0]
            for r in rows:
                if tuple(r.get("token_ids") or []) != majority:
                    slot_of_minority[r["prompt_id"].rsplit("-s", 1)[-1]] += 1
    return dis, agr, slot_of_minority


def main() -> int:
    argv = sys.argv[1:]
    lane, out_path, roots = "ladder-mtp0", None, []
    i = 0
    while i < len(argv):
        if argv[i] == "--lane":
            lane = argv[i + 1]; i += 2
        elif argv[i] == "--json":
            out_path = Path(argv[i + 1]); i += 2
        else:
            roots.append(Path(argv[i])); i += 1
    report = {}
    for root in roots:
        dis, agr, slots = analyse(root, lane)
        if not dis:
            print(f"{root.name}: no disagreeing groups")
            continue
        ds = [d["spread_s"] for d in dis]
        print(f"=== {root.name} ===")
        print(f"  disagreeing groups: {len(dis)}   agreeing groups sampled: {len(agr)}")
        print(f"  token-arrival spread at the divergence index: "
              f"median {statistics.median(ds)*1000:.1f} ms, max {max(ds)*1000:.1f} ms")
        if agr:
            print(f"  spread among copies that agree:                median "
                  f"{statistics.median(agr)*1000:.1f} ms, max {max(agr)*1000:.1f} ms")
        print(f"  divergence indices: {sorted({d['index'] for d in dis})}")
        print(f"  minority-output slots (top): {slots.most_common(6)}")
        report[root.name] = {
            "disagreeing_groups": len(dis),
            "median_spread_ms_at_divergence": round(statistics.median(ds) * 1000, 2),
            "max_spread_ms_at_divergence": round(max(ds) * 1000, 2),
            "median_spread_ms_when_agreeing": round(statistics.median(agr) * 1000, 2) if agr else None,
            "divergence_indices": sorted({d["index"] for d in dis}),
            "minority_slot_counts": dict(slots.most_common()),
        }
    if out_path is not None:
        out_path.write_text(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
