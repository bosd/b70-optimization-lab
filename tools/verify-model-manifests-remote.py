#!/usr/bin/env python3
"""Check every pinned model manifest against its publisher repository, without downloading weights.

The recipes hand out a Hugging Face repository, an immutable revision, and per-file sizes and SHA-256 digests. This
walks the tracked manifests, asks the Hub for that exact revision, and reports whether the repository still exists,
the revision still resolves, and every pinned file still matches. Metadata only: a full pass costs a few seconds and
no bandwidth, so it can run whenever the catalogue changes.

usage: verify-model-manifests-remote.py [--json OUT] [PATH ...]
exit 0 when every manifest verifies, 1 otherwise.
"""
from __future__ import annotations
import argparse, glob, json, sys, urllib.error, urllib.request

API = "https://huggingface.co/api/models/{repo}/revision/{rev}?blobs=true"


def load(path: str):
    try:
        return json.load(open(path))
    except (OSError, ValueError) as exc:
        return {"__error__": str(exc)}


def pinned(doc) -> tuple[str | None, str | None, list[dict]]:
    """Return (repository, revision, files) for the manifest shapes the lab uses."""
    if not isinstance(doc, dict):
        return None, None, []
    repo = doc.get("repository") or doc.get("hf_id") or doc.get("repo")
    rev = doc.get("revision") or doc.get("sha")
    files = doc.get("lfs_files") or doc.get("files") or []
    if isinstance(repo, dict):
        repo, rev = repo.get("id") or repo.get("repository"), rev or repo.get("revision")
    # Entries marked origin=derived-locally are built on the host (a relabel, a requantization) and are
    # deliberately absent upstream, so they are the local verifier's business, not the publisher's.
    files = [f for f in files if isinstance(f, dict) and f.get("path") and f.get("sha256")
             and str(f.get("origin", "publisher")).startswith("publisher")]
    return repo, rev, files


def fetch(repo: str, rev: str):
    req = urllib.request.Request(API.format(repo=repo, rev=rev), headers={"User-Agent": "b70-lab-manifest-check"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def check(path: str) -> dict:
    doc = load(path)
    if "__error__" in doc:
        return {"manifest": path, "state": "unreadable", "detail": doc["__error__"]}
    repo, rev, files = pinned(doc)
    derived = sum(1 for f in (doc.get("lfs_files") or []) if isinstance(f, dict) and not str(f.get("origin", "publisher")).startswith("publisher"))
    if not repo or not rev:
        return {"manifest": path, "state": "skipped", "detail": "no repository/revision pin"}
    if not files:
        return {"manifest": path, "state": "skipped", "repository": repo, "revision": rev, "detail": "no per-file digests"}
    try:
        remote = fetch(repo, rev)
    except urllib.error.HTTPError as exc:
        return {"manifest": path, "state": "unreachable", "repository": repo, "revision": rev, "detail": f"HTTP {exc.code}"}
    except Exception as exc:  # noqa: BLE001 - network shapes vary
        return {"manifest": path, "state": "unreachable", "repository": repo, "revision": rev, "detail": str(exc)[:120]}
    if remote.get("sha") != rev:
        return {"manifest": path, "state": "revision-moved", "repository": repo, "revision": rev, "detail": f"resolved to {remote.get('sha')}"}
    have = {s["rfilename"]: s for s in remote.get("siblings", []) if s.get("lfs")}
    problems = []
    for f in files:
        r = have.get(f["path"])
        if r is None:
            problems.append(f"{f['path']}: absent at this revision")
            continue
        if r["lfs"].get("sha256") != f["sha256"]:
            problems.append(f"{f['path']}: sha256 differs")
        elif f.get("bytes") and r["lfs"].get("size") != f["bytes"]:
            problems.append(f"{f['path']}: byte size differs")
    return {"manifest": path, "state": "ok" if not problems else "mismatch", "repository": repo, "revision": rev,
            "files_checked": len(files), "derived_skipped": derived, **({"problems": problems} if problems else {})}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--json", dest="out")
    a = ap.parse_args()
    paths = a.paths or sorted(set(glob.glob("repro/*/manifests/*.json") + glob.glob("repro/*/model-manifest.json") + glob.glob("experiments/*/manifests/*.json")))
    results = [check(p) for p in paths]
    order = {"mismatch": 0, "revision-moved": 1, "unreachable": 2, "unreadable": 3, "ok": 4, "skipped": 5}
    for r in sorted(results, key=lambda r: (order.get(r["state"], 9), r["manifest"])):
        line = f"{r['state']:<14} {r['manifest']}"
        if r.get("repository"):
            line += f"  {r['repository']}@{str(r.get('revision'))[:12]}"
        if r.get("files_checked"):
            line += f"  ({r['files_checked']} files"
            line += f", {r['derived_skipped']} derived skipped)" if r.get("derived_skipped") else ")"
        if r.get("detail"):
            line += f"  {r['detail']}"
        print(line)
        for p in r.get("problems", []):
            print(f"    - {p}")
    counts = {}
    for r in results:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    print("\n" + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if a.out:
        json.dump({"results": results, "counts": counts}, open(a.out, "w"), indent=1)
    return 0 if not (counts.get("mismatch") or counts.get("revision-moved") or counts.get("unreachable") or counts.get("unreadable")) else 1


if __name__ == "__main__":
    sys.exit(main())
