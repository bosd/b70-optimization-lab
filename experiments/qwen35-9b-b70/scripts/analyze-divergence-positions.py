#!/usr/bin/env python3
"""Characterise where and how concurrent requests diverge from the sequential oracle.

The powered arms establish a divergence rate but say nothing about the divergences themselves. This
reads the token arrays already captured in each ladder and reports, for every divergent request, the
position of the first differing token and the pair of token ids substituted there.

That is the cheap half of the question the identity ladders cannot answer: whether these are single
isolated substitutions or the point where two continuations part, and whether the same token pairs
recur - which is what a near-tie between two specific candidates would look like.

Needs no GPU: everything is already in the ladder files.

usage: analyze-divergence-positions.py ROOT [ROOT ...] [--lane ladder-mtp0] [--json OUT]
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def analyse(root: Path, lane: str):
    p = root / lane / "ladder.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text())
    oracle = {r["prompt_id"]: r.get("token_ids") or [] for r in (d.get("oracle") or {}).get("rows", [])}
    out = []
    for b in d["batches"]:
        for r in b["rows"]:
            ref = oracle.get(r["prompt_id"])
            got = r.get("token_ids") or []
            if not ref or ref == got:
                continue
            first = next((i for i, (x, y) in enumerate(zip(ref, got)) if x != y), min(len(ref), len(got)))
            out.append({
                "pass": b["repeat"], "prompt_id": r["prompt_id"],
                "first_diff_index": first,
                "oracle_len": len(ref), "got_len": len(got),
                "oracle_token": ref[first] if first < len(ref) else None,
                "got_token": got[first] if first < len(got) else None,
                "tail_identical_after_diff": ref[first + 1:] == got[first + 1:],
            })
    return out


def main() -> int:
    argv = sys.argv[1:]
    lane = "ladder-mtp0"
    out_path = None
    roots: list[Path] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--lane":
            lane = argv[i + 1]; i += 2
        elif argv[i] == "--json":
            out_path = Path(argv[i + 1]); i += 2
        else:
            roots.append(Path(argv[i])); i += 1
    if not roots:
        print(__doc__)
        return 2
    report = {}
    for root in roots:
        ev = analyse(root, lane)
        if ev is None:
            print(f"{root.name}: no {lane}")
            continue
        report[root.name] = ev
        print(f"=== {root.name}: {len(ev)} divergent request(s) ===")
        for e in ev:
            frac = e["first_diff_index"] / max(e["oracle_len"], 1)
            print(f"  pass{e['pass']} {e['prompt_id'][:26]:28} first diff at token "
                  f"{e['first_diff_index']:>3}/{e['oracle_len']:<4} ({frac:>4.0%})  "
                  f"{e['oracle_token']} -> {e['got_token']}  "
                  f"{'rest identical' if e['tail_identical_after_diff'] else 'rest differs'}")
    allev = [e for ev in report.values() for e in ev]
    if allev:
        pairs = collections.Counter((e["oracle_token"], e["got_token"]) for e in allev)
        prompts = collections.Counter(e["prompt_id"] for e in allev)
        single = sum(1 for e in allev if e["tail_identical_after_diff"])
        print(f"\nacross {len(allev)} divergences in {len(report)} arm(s):")
        print(f"  single-token substitutions (rest identical): {single}/{len(allev)}")
        print(f"  distinct token pairs: {len(pairs)}; most common: {pairs.most_common(3)}")
        print(f"  distinct prompts: {len(prompts)}; most common: {prompts.most_common(3)}")
        report["_summary"] = {"divergences": len(allev), "single_token_substitutions": single,
                              "distinct_token_pairs": len(pairs),
                              "token_pair_counts": {f"{a}->{b}": n for (a, b), n in pairs.most_common()},
                              "prompt_counts": dict(prompts.most_common())}
    if out_path is not None:
        out_path.write_text(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
