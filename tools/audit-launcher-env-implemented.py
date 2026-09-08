#!/usr/bin/env python3
"""Which environment variables the launchers forward does the image actually implement?

Three experiments in one session were run and written up before it was noticed that the knob under
test never reached the container. A fourth class of the same mistake is available: a knob that
reaches the container and is read by nothing, because it belongs to a different image's patch series.
`VLLM_XPU_W8A16_DECODE_PAD_ROWS`, the R65 batch-invariant lm_head and the four GDN trace hooks are all
forwarded by the published launchers and absent from R276.

A recorded container environment showing `KNOB=0` reads as a deliberate setting. If nothing reads it,
it is not a setting at all, and an arm that flips it is a null. This lists which is which.

usage: audit-launcher-env-implemented.py IMAGE [--json OUT]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAUNCHERS = [
    ROOT / "repro/qwen38-27b-fp8-vllm-tp2-asrock-b70/run-server.sh",
    ROOT / "repro/qwen38-27b-fp8-vllm-tp2-asrock-b70/run-w8a16-mtp1-server.sh",
]
ENV_RE = re.compile(r'(?:--env|-e)\s+"?([A-Z_][A-Z0-9_]*)=')
# Consumed by the harness or the serve command line rather than by library code.
HARNESS_OWNED = {"REPRO_TP", "REPRO_QUANTIZATION", "REPRO_MAX_NUM_SEQS", "REPRO_MAX_MODEL_LEN",
                 "REPRO_MAX_BATCHED_TOKENS", "REPRO_GPU_MEMORY_UTILIZATION",
                 "REPRO_SERVED_MODEL_NAME", "REPRO_COMPILATION_CONFIG"}


def forwarded() -> set[str]:
    names: set[str] = set()
    for p in LAUNCHERS:
        if p.exists():
            names |= set(ENV_RE.findall(p.read_text()))
    return names - HARNESS_OWNED


def implemented(image: str, names: list[str]) -> dict[str, str]:
    """Ask the image once whether each name appears anywhere under site-packages."""
    script = "; ".join(
        f'printf "%s %s\\n" {n} "$(grep -rl {n} /opt/venv/lib/python3.12/site-packages/ 2>/dev/null | head -1)"'
        for n in names
    )
    out = subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", "bash", image, "-lc", script],
        capture_output=True, text=True, timeout=1800,
    )
    found = {}
    for line in out.stdout.splitlines():
        parts = line.split(None, 1)
        if parts:
            found[parts[0]] = parts[1].strip() if len(parts) > 1 else ""
    return found


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    image = args[0]
    names = sorted(forwarded())
    where = implemented(image, names)
    live = {n: where[n] for n in names if where.get(n)}
    inert = [n for n in names if not where.get(n)]
    print(f"image: {image}")
    print(f"forwarded by the launchers: {len(names)}   implemented: {len(live)}   inert: {len(inert)}\n")
    if inert:
        print("Forwarded but read by nothing in this image. Flipping these changes nothing; note that")
        print("this does not say the behaviour is off - a patch series may have made it unconditional")
        print("at build time - only that the variable no longer controls it:")
        for n in inert:
            print(f"  {n}")
    report = {"image": image, "forwarded": names,
              "implemented": {n: where[n].replace("/opt/venv/lib/python3.12/site-packages/", "") for n in live},
              "inert": inert}
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
