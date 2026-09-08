#!/usr/bin/env python3
"""Rebuild a Q38_EXPERT_HOST_PLACEMENT JSON from a lineage's own routing census.

The 2026-09-06 placement parked (layer, expert) pairs that a top-k dump taken on the
torch-fallback line had never selected. A311 showed that survey is stale for the fused-QSA
line: parked experts are selected on 1.0-1.1% of routed blocks on three ranks and 17.5% on
the rank holding the hot experts, and every such selection is a PCIe read of a whole expert
row. The census (Q38_PLACEMENT_HIT_CENSUS=1) counts every routed expert on the lineage
under test and writes one JSON per rank; this builder parks the coldest pairs by those
counts, under the same byte budget and the same even layer fill as the original builder.

It also reports what the change is expected to buy: the host selections the old placement
took during the census run, against the host selections the new placement would have taken
on the same routing. Selecting which weights live in which memory does not touch the
arithmetic, so a corrected placement is an exact lever.

  build-q38-expert-host-placement-from-census.py --census /tmp/q38-a313-census-rank0.json \
      [--census ...] --host-gib-per-rank 3.5 --out <path> [--compare <old placement>]
"""
from __future__ import annotations

import argparse
import json
import re


def load_census(paths: list[str]) -> tuple[dict, dict]:
    """{rank: {layer: {local expert: count}}} plus the parked set each rank ran with."""
    counts: dict[int, dict[int, dict[int, int]]] = {}
    parked: dict[int, dict[int, set[int]]] = {}
    for path in paths:
        m = re.search(r"rank(\d+)\.json$", path)
        if not m:
            raise SystemExit(f"cannot read a rank from {path}")
        rank = int(m.group(1))
        raw = json.load(open(path))
        c = counts.setdefault(rank, {})
        p = parked.setdefault(rank, {})
        for layer, entry in raw.items():
            L = int(layer)
            c.setdefault(L, {})
            for e, n in entry.get("counts", {}).items():
                c[L][int(e)] = c[L].get(int(e), 0) + int(n)
            if entry.get("host"):
                p[L] = set(int(e) for e in entry["host"])
    return counts, parked


def load_dump_hits(paths: list[str], experts_per_rank: int) -> set[tuple[int, int, int]]:
    """{(rank, layer, local expert)} selected in an earlier decode-sized top-k dump."""
    if not paths:
        return set()
    import re as _re

    import torch

    hit: set[tuple[int, int, int]] = set()
    for path in paths:
        for name, ids in torch.load(path, weights_only=False, map_location="cpu"):
            m = _re.search(r"layers\.(\d+)\.", str(getattr(name, "value", name)))
            if not m:
                continue
            layer = int(m.group(1))
            for row in ids.tolist():
                for e in row:
                    e = int(e)
                    hit.add((e // experts_per_rank, layer, e % experts_per_rank))
    return hit


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--census", action="append", required=True)
    ap.add_argument("--host-gib-per-rank", type=float, required=True)
    ap.add_argument("--layers", type=int, default=48)
    ap.add_argument("--experts-per-rank", type=int, default=128)
    ap.add_argument("--bytes-per-expert", type=int, default=1280 * 2560 + 2560 * 640)
    ap.add_argument("--max-count", type=int, default=0,
                    help="park only pairs selected at most this many times on this lineage "
                         "(0 = the original never-hit policy; a parked pair that is selected "
                         "costs a PCIe read of a whole expert row)")
    ap.add_argument("--exclude-hits-from", action="append", default=[],
                    help="a moe-topk-ids .pt dump whose hits also disqualify a pair. Use it to "
                         "park only pairs that neither this lineage nor an earlier one ever "
                         "selected, which is safer for workloads unlike the census request")
    ap.add_argument("--compare", help="the placement the census run used, for the before/after count")
    ap.add_argument("--match-compare-shape", action="store_true",
                    help="park exactly as many experts per (rank, layer) as --compare does, "
                         "choosing the coldest by this census. Host bytes and therefore VRAM "
                         "are then identical to the compared placement, so the only variable "
                         "is which experts are parked")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    counts, parked = load_census(a.census)
    budget = int(a.host_gib_per_rank * 2**30) // a.bytes_per_expert
    per_layer = budget // a.layers + 1
    old = json.load(open(a.compare)) if a.compare else None
    excluded = load_dump_hits(a.exclude_hits_from, a.experts_per_rank)
    if excluded:
        print(f"excluding {len(excluded)} (rank, layer, expert) pairs hit in "
              f"{len(a.exclude_hits_from)} earlier dump(s)")

    out: dict[str, dict[str, list[int]]] = {}
    for rank in sorted(counts):
        placement: dict[str, list[int]] = {}
        total = 0
        seen_before = seen_after = routed = 0
        for L in range(a.layers):
            layer_counts = counts[rank].get(L, {})
            if not layer_counts and L not in parked.get(rank, {}):
                continue
            cand = sorted((layer_counts.get(e, 0), e) for e in range(a.experts_per_rank)
                          if (rank, L, e) not in excluded)
            room = max(0, budget - total)
            if a.match_compare_shape:
                if old is None:
                    raise SystemExit("--match-compare-shape needs --compare")
                want = len(old.get(str(rank), {}).get(str(L), []))
                chosen = [e for _, e in cand[:want]]
            else:
                chosen = [e for c, e in cand[:per_layer] if c <= a.max_count][:room]
            if chosen:
                placement[str(L)] = sorted(chosen)
                total += len(chosen)
            routed += sum(layer_counts.values())
            seen_after += sum(layer_counts.get(e, 0) for e in chosen)
            was = parked.get(rank, {}).get(L, set())
            if old is not None:
                was = set(old.get(str(rank), {}).get(str(L), [])) or was
            seen_before += sum(layer_counts.get(e, 0) for e in was)
        out[str(rank)] = placement
        cold = sum(1 for L in counts[rank] for e in range(a.experts_per_rank)
                   if counts[rank][L].get(e, 0) == 0)
        print(f"rank {rank}: placed {total} of a {budget}-expert budget "
              f"({total * a.bytes_per_expert / 2**30:.2f} GiB) "
              f"across {len(placement)} layers; never selected on this lineage: {cold} pairs; "
              f"host selections during the census {seen_before} -> {seen_after} "
              f"of {routed} routed ({100.0 * seen_before / max(routed, 1):.3f}% -> "
              f"{100.0 * seen_after / max(routed, 1):.3f}%)")
    json.dump(out, open(a.out, "w"), indent=0)
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
