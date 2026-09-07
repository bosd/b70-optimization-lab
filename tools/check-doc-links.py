#!/usr/bin/env python3
"""Check that repository-relative links inside the guides and site pages point at files that exist.

Covers Markdown links and HTML hrefs whose target is a path in this repository (not http, mailto or a bare anchor).
Link rot here is silent: a renamed evidence file leaves a guide pointing at nothing, and nobody notices until a reader
tries to follow it. Offline and fast, so it can run on every change.

usage: check-doc-links.py [--json OUT] [PATH ...]
exit 0 when every link resolves, 1 otherwise.
"""
from __future__ import annotations
import argparse, glob, json, os, re, sys, urllib.parse

MD = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HREF = re.compile(r"(?:href|src)=\"([^\"]+)\"")
SKIP = ("http://", "https://", "mailto:", "data:", "#", "javascript:", "tel:")


def targets(path: str):
    text = open(path, encoding="utf-8", errors="replace").read()
    pat = MD if path.endswith(".md") else HREF
    for m in pat.finditer(text):
        yield m.group(1)


def check_file(path: str, root: str):
    bad = []
    for raw in targets(path):
        # Skip template placeholders: generated pages contain JavaScript literals like models/${id}.html
        if raw.startswith(SKIP) or not raw.strip() or "${" in raw or "{{" in raw:
            continue
        link = urllib.parse.unquote(raw.split("#", 1)[0].split("?", 1)[0])
        if not link:
            continue
        base = root if link.startswith("/") else os.path.dirname(path)
        resolved = os.path.normpath(os.path.join(base, link.lstrip("/")))
        if not os.path.exists(resolved):
            bad.append({"link": raw, "resolved": os.path.relpath(resolved, root)})
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--json", dest="out")
    a = ap.parse_args()
    root = os.getcwd()
    paths = a.paths or sorted(
        glob.glob("*.md") + glob.glob("*.html")
        + glob.glob("repro/**/*.md", recursive=True)
        + glob.glob("packages/**/*.md", recursive=True)
        + glob.glob("learn/*.html") + glob.glob("docs/**/*.md", recursive=True)
        + glob.glob("results/**/*.md", recursive=True)
    )
    findings = {}
    for p in paths:
        bad = check_file(p, root)
        if bad:
            findings[p] = bad
    total = sum(len(v) for v in findings.values())
    for p, bad in sorted(findings.items()):
        print(f"{p}: {len(bad)} broken")
        for b in bad[:8]:
            print(f"    - {b['link']}  ->  {b['resolved']}")
        if len(bad) > 8:
            print(f"    ... {len(bad) - 8} more")
    print(f"\nchecked {len(paths)} documents, {total} broken repository-relative link(s) in {len(findings)} file(s)")
    if a.out:
        json.dump({"documents_checked": len(paths), "broken_total": total, "findings": findings}, open(a.out, "w"), indent=1)
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
