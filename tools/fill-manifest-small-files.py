#!/usr/bin/env python3
"""Populate a model manifest's `small_files` from the publisher API at the pinned revision.

A manifest whose `small_files` is empty pins only the weights. That leaves the configuration files
unverified and, worse, makes the recipe's own download step produce a directory that cannot load.
For a compressed-tensors checkpoint `config.json` carries the quantization config that selects the
kernel route, so these files are part of the measured identity, not packaging noise.

Non-LFS files are identified by their git blob SHA-1, which is what the publisher API reports for
them; LFS files keep their SHA-256 and are never touched here.

usage: fill-manifest-small-files.py MANIFEST [MANIFEST ...] [--dry-run]
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

API = "https://huggingface.co/api/models/{repo}/tree/{rev}?recursive=1"


def tree(repo: str, rev: str) -> list[dict]:
    req = urllib.request.Request(API.format(repo=repo, rev=rev), headers={"User-Agent": "b70-lab-manifest/1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        print(__doc__)
        return 2
    rc = 0
    for path in args:
        p = Path(path)
        m = json.loads(p.read_text())
        repo, rev = m["repository"], m["revision"]
        listed_lfs = {f["path"] for f in (m.get("lfs_files") or [])}
        entries = tree(repo, rev)

        small, lfs_seen = [], set()
        for e in entries:
            if e.get("type") != "file":
                continue
            if e.get("lfs"):
                lfs_seen.add(e["path"])
                continue
            small.append({"path": e["path"], "bytes": e["size"], "git_blob": e["oid"]})
        small.sort(key=lambda f: f["path"])

        unlisted = sorted(lfs_seen - listed_lfs)
        missing = sorted(listed_lfs - lfs_seen)
        before = len(m.get("small_files") or [])
        print(f"{p}\n  repo {repo}@{rev[:12]}  small_files {before} -> {len(small)}")
        if unlisted:
            print(f"  WARNING: publisher LFS files absent from this manifest: {unlisted}")
            rc = 1
        if missing:
            print(f"  WARNING: manifest lists LFS files the publisher does not have: {missing}")
            rc = 1
        if dry:
            for f in small:
                print(f"    + {f['path']} ({f['bytes']} bytes)")
            continue
        m["small_files"] = small
        p.write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
