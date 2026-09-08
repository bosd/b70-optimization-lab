#!/usr/bin/env python3
"""Verify that every repo-relative path inside the JSON manifests actually exists.

`tools/check-doc-links.py` validates links in Markdown. It cannot see the paths that live
inside JSON: a family manifest's `evidence` lists, a package's `dependencies`, the guide and
attestation pointers in `packages/catalog.json`. Those are how a reader gets from a published
number to the file that supports it, so a stale one is a broken claim rather than a broken
link.

Walks families/*.json, packages/*/package.json and packages/catalog.json, treats any string
that looks like a repo-relative path under a known top-level directory as a claim, and checks
it resolves. Exits non-zero if any does not.

  python3 tools/check-manifest-paths.py [--verbose]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOP = ("experiments", "results", "repro", "packages", "patches", "data", "scripts", "tools",
       "configs", "families", "notes", "docs", "benchmarks", "models", "claims", "audits")
PATH_RE = re.compile(r"^(?:%s)/[\w./\-\[\]=,()+]+$" % "|".join(TOP))


def walk(node, src, out):
    if isinstance(node, dict):
        for v in node.values():
            walk(v, src, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, src, out)
    elif isinstance(node, str) and PATH_RE.match(node):
        out.append((src, node))


def main() -> int:
    verbose = "--verbose" in sys.argv
    files = sorted(ROOT.glob("families/*.json")) + sorted(ROOT.glob("packages/*/package.json"))
    catalog = ROOT / "packages/catalog.json"
    if catalog.exists():
        files.append(catalog)
    claims: list[tuple[str, str]] = []
    for f in files:
        try:
            walk(json.loads(f.read_text()), str(f.relative_to(ROOT)), claims)
        except json.JSONDecodeError as exc:
            print(f"unreadable JSON: {f.relative_to(ROOT)}: {exc}", file=sys.stderr)
            return 2
    missing = [(s, p) for s, p in claims if not (ROOT / p).exists()]
    print(f"checked {len(claims)} repo-relative paths in {len(files)} manifests; "
          f"{len(missing)} missing")
    for s, p in missing:
        print(f"  MISSING  {s}: {p}")
    if verbose and not missing:
        for s, p in claims[:10]:
            print(f"  ok  {s}: {p}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
