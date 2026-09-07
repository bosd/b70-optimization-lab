#!/usr/bin/env python3
"""Static checks for generated container packets.

compose.yaml is generated from the recipe launcher so the packet cannot drift away from the
configuration that produced the measured result. These checks defend that property in CI, where the
image and the model weights are not available and the generator cannot be re-run:

  * the image is pinned by digest, never by a floating tag;
  * the model is mounted read-only and the port is bound to loopback;
  * both card-count profiles exist and differ only in device selection and tensor parallel size;
  * every environment variable the launcher sets statically is present in compose.yaml, so adding a
    variable to the launcher without regenerating the packet fails the build.

usage: check-container-packet.py [PACKET_DIR ...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required for check-container-packet.py", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
LAUNCHERS = [
    ROOT / "repro/qwen38-27b-fp8-vllm-tp2-asrock-b70/run-w8a16-mtp1-server.sh",
    ROOT / "repro/qwen38-27b-fp8-vllm-tp2-asrock-b70/run-w8a16-mtp1-strict-server.sh",
]
ENV_RE = re.compile(r"--env\s+\"?([A-Z_][A-Z0-9_]*)=")
# Set by the wrapper's `env` prologue rather than passed through to the container.
NOT_FORWARDED = {
    "IMAGE", "EXPECTED_IMAGE_ID", "EXPECTED_KERNEL_HEAD", "GPU_MEMORY_UTILIZATION",
    "ENFORCE_EAGER", "COMPILATION_CONFIG", "VLLM_USE_V2_MODEL_RUNNER",
}


def launcher_env_names() -> set[str]:
    """Environment variables the launcher forwards unconditionally.

    Some variables are forwarded only when the operator sets them (the W4A16 pad-low knob, the
    fixed-K overrides). Those are legitimately absent from a packet that does not use them, so a
    line that guards its `--env` behind a conditional does not contribute a requirement.
    """
    names: set[str] = set()
    for p in LAUNCHERS:
        if not p.exists():
            continue
        for line in p.read_text().splitlines():
            found = ENV_RE.findall(line)
            if not found:
                continue
            stripped = line.strip()
            conditional = stripped.startswith(("if ", "elif ")) or "; then" in stripped
            if not conditional:
                names |= set(found)
    return names - NOT_FORWARDED


def check(packet: Path) -> list[str]:
    errs: list[str] = []
    compose = packet / "compose.yaml"
    if not compose.exists():
        return [f"{packet.name}: compose.yaml is missing"]
    doc = yaml.safe_load(compose.read_text())
    services = doc.get("services") or {}

    for name in ("one-gpu", "two-gpu"):
        if name not in services:
            errs.append(f"{packet.name}: compose.yaml has no {name} service")
    if errs:
        return errs

    envs, cmds = {}, {}
    for name, svc in services.items():
        image = svc.get("image") or (doc.get("x-b70-common") or {}).get("image", "")
        if "@sha256:" not in image:
            errs.append(f"{packet.name}/{name}: image is not pinned by digest: {image!r}")
        vols = svc.get("volumes") or (doc.get("x-b70-common") or {}).get("volumes") or []
        if not any(str(v).endswith(":/model:ro") for v in vols):
            errs.append(f"{packet.name}/{name}: the model is not mounted read-only at /model")
        for port in svc.get("ports") or []:
            if not str(port).startswith("127.0.0.1:"):
                errs.append(f"{packet.name}/{name}: port {port!r} is not bound to loopback")
        envs[name] = dict(svc.get("environment") or {})
        cmds[name] = [str(c) for c in (svc.get("command") or [])]

    want = launcher_env_names()
    for name, env in envs.items():
        missing = sorted(want - set(env))
        if missing:
            errs.append(
                f"{packet.name}/{name}: compose.yaml is missing {len(missing)} launcher "
                f"environment variable(s), regenerate the packet: {missing[:6]}"
            )

    differing = {k for k in set(envs["one-gpu"]) | set(envs["two-gpu"])
                 if envs["one-gpu"].get(k) != envs["two-gpu"].get(k)}
    if differing != {"ZE_AFFINITY_MASK", "ONEAPI_DEVICE_SELECTOR"}:
        errs.append(
            f"{packet.name}: the two profiles should differ only in device selection, "
            f"but differ in {sorted(differing)}"
        )

    def arg(cmd: list[str], flag: str) -> str | None:
        return cmd[cmd.index(flag) + 1] if flag in cmd and cmd.index(flag) + 1 < len(cmd) else None

    if arg(cmds["one-gpu"], "--tensor-parallel-size") != "1":
        errs.append(f"{packet.name}/one-gpu: tensor parallel size is not 1")
    if arg(cmds["two-gpu"], "--tensor-parallel-size") != "2":
        errs.append(f"{packet.name}/two-gpu: tensor parallel size is not 2")
    for name, cmd in cmds.items():
        one = [c for c in cmd if c != arg(cmd, "--tensor-parallel-size")]
        if "--no-enable-prefix-caching" not in cmd:
            errs.append(f"{packet.name}/{name}: prefix caching is not disabled; results would not be cache-zero")
        del one
    return errs


def main() -> int:
    packets = [Path(a) for a in sys.argv[1:]] or sorted(
        p.parent for p in ROOT.glob("packages/*/compose.yaml")
    )
    if not packets:
        print("no container packets found (nothing with a compose.yaml)")
        return 0
    failed = 0
    for packet in packets:
        errs = check(packet)
        if errs:
            failed += 1
            for e in errs:
                print(f"FAIL {e}")
        else:
            print(f"ok   {packet.name}: container packet consistent with the recipe launcher")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
