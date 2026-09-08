#!/usr/bin/env python3
"""Exercise the repo's SHA256 pins on tracked files, so drift is found before a gate is.

A record gate that pins a shared tool by hash only fails when someone runs it. The Laguna
record's gate pinned `scripts/bench-openai-realistic-suite.py` and had been unrunnable since
2026-08-25; nothing surfaced it for two weeks because nobody replayed that record. The
Flash-Next audit found 224 frozen clients in the same state, and only because something
finally ran them. An unexercised guarantee is indistinguishable from a satisfied one.

This checks the pins that can be checked cheaply: literal `sha256sum <repo-relative path>`
comparisons against a 64-hex constant, in shell under repro/, experiments/ and scripts/. It
deliberately does not resolve shell variables, so a pin on "$server" is reported as unchecked
rather than guessed at -- a wrong answer here is worse than an absent one.

Drift is not automatically a defect: a frozen packet SHOULD pin the tool it was verified
against, and shared tooling legitimately moves. What this gives is the list, with the fact
stated, so the decision is deliberate.

  python3 tools/check-pinned-hashes.py [--quiet]
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOTS = ("repro", "experiments", "scripts", "tools")
# sha256sum <path> ... == <64 hex>, where <path> is a literal repo-relative or repo-rooted path
PIN = re.compile(
    r"sha256sum\s+(?:--\s+)?[\"']?(?:\$\{?repo(?:_root)?\}?/|\$\{?ROOT\}?/)?"
    r"((?:repro|experiments|scripts|tools|configs|data|patches)/[^\"'$\s|]+)[\"']?"
    r"[^=\n]{0,80}==\s*[\"']?([0-9a-f]{64})"
)


def main() -> int:
    quiet = "--quiet" in sys.argv
    checked = ok = drifted = absent = 0
    findings: list[tuple[str, str, str]] = []
    for top in ROOTS:
        for f in (ROOT / top).rglob("*.sh"):
            try:
                text = f.read_text(errors="ignore")
            except OSError:
                continue
            for rel, want in PIN.findall(text):
                checked += 1
                target = ROOT / rel
                if not target.exists():
                    absent += 1
                    findings.append(("ABSENT", str(f.relative_to(ROOT)), rel))
                    continue
                got = hashlib.sha256(target.read_bytes()).hexdigest()
                if got == want:
                    ok += 1
                else:
                    drifted += 1
                    findings.append(("DRIFT", str(f.relative_to(ROOT)), rel))
    print(f"checked {checked} literal file pins: {ok} match, {drifted} drifted, {absent} target absent")
    if not quiet:
        seen = set()
        for kind, holder, rel in findings:
            key = (kind, rel)
            if key in seen:
                continue
            seen.add(key)
            print(f"  {kind:6s} {rel}")
            print(f"         pinned by {holder}")
    return 1 if (drifted or absent) else 0


if __name__ == "__main__":
    raise SystemExit(main())
