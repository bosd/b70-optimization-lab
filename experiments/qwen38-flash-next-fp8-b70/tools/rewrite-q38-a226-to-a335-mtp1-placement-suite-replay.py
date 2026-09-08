#!/usr/bin/env python3
"""Create the A335 replay of A226, the placement lossless-MTP1 record (31.929484).\n\nFour of the lane's five published Flash-Next records have now been re-measured. This is the\noldest MTP1 line still unreplayed, on overlay 005dc578 -- the never-hit expert host placement\nbefore either reference Triton kernel was restored. Older lines are where drift is most\nlikely, since more tooling has moved underneath them.\n\nPure replay: certified map, certified verifier, nothing changed but attempt and port."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A335_REWRITE_VALIDATE_ONLY") == "1"
SOURCES = {
    'launch-tp4-mtp1-4352-ple-only-a226-fullgraphdet-w13n32.sh': '2734f9d22406fb29074849e544681857d8b7aa3f70dbf2d82195d25d8ade3be8',
    'run-tp4-mtp1-4352-ple-only-a226-fullgraphdet-w13n32-client.sh': '8279051e2c4a8547a0dae9f1daf8bb9553ae0cbcb0f70befc5fa00312a05c8c0',
    'supervise-tp4-mtp1-4352-ple-only-a226-fullgraphdet-w13n32.sh': '1685c7844dcbf6fcdbf9e23619a694d2a8ff9a8f9b1eaa2aac8b299438ea3364',
    'run-q38-a226-host-controlled.sh': 'e0d1c3a362615b2d97cc23fa3c96b0b0dd7a00e915a628ebefd16f127dc880ac',
}
HASH_TOKEN = re.compile(r"[0-9a-f]{64}|[0-9a-f]{40}")
OLD_HEAD = "005dc57895896f770157ea94f68e473e7447139e"
NEW_HEAD = OLD_HEAD  # no source change: 64 is already an allowed tile
OLD_MAP_SHA = "a8f1f8982e3e1af80ff31b9e0a00afaacf1af1b3c401585109b4d60d3c8267be"
NEW_MAP_SHA = OLD_MAP_SHA  # replay of the superseded line: certified map unchanged
OLD_VERIFIER_SHA = "c874852bbae20f4d738e1f3a37f1b16d553e50dc9e8c56c2b0caabc22675dc0e"
NEW_VERIFIER_SHA = OLD_VERIFIER_SHA  # unchanged

def digest(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()

def source(name):
    data = (ROOT / name).read_bytes()
    assert digest(data) == SOURCES[name], name
    return data.decode()

def successor(text):
    def rename(seg):
        seg = seg.replace("tp4-mtp1-4352-ple-only-a226", "tp4-mtp1-4352-ple-only-a335")
        seg = seg.replace("attempt226", "attempt335").replace("19896", "19948")
        seg = seg.replace("ATTEMPT=226", "ATTEMPT=335").replace("a226", "a335").replace("A226", "A335")
        seg = seg.replace("moe-m1-w13-n32", "moe-m1-w13-n32")
        seg = seg.replace("verify-moe-m1-w13-n32-selection", "verify-moe-m1-w13-n32-selection")
        seg = seg.replace("W13-N32", "W13-N32").replace("w13n32", "w13n32")
        return seg
    parts, last = [], 0
    for m in HASH_TOKEN.finditer(text):
        parts.append(rename(text[last:m.start()]))
        parts.append(m.group(0))
        last = m.end()
    parts.append(rename(text[last:]))
    out = "".join(parts)
    assert sorted(HASH_TOKEN.findall(out)) == sorted(HASH_TOKEN.findall(text))
    assert "ATTEMPT=335" in out or "ATTEMPT=" not in out, "the attempt number did not move"
    # Check the renamed text only: a sha256 token can contain the digits of the old port,
    # and rename deliberately does not touch hashes.
    stripped = HASH_TOKEN.sub("", out)
    assert "19970" not in stripped and "attempt226" not in stripped and "a226" not in stripped
    # A replay of the superseded line keeps the certified map, so its name survives.
    return out

def replace_n(t, a, b, n):
    assert t.count(a) == n, (t.count(a), a[:90])
    return t.replace(a, b)

def emit(name, text):
    p = ROOT / name
    if VALIDATE_ONLY:
        assert p.read_text() == text, name
        return
    assert not p.exists(), p
    p.write_text(text)
    p.chmod(0o755)

def main():
    launcher = source("launch-tp4-mtp1-4352-ple-only-a226-fullgraphdet-w13n32.sh")
    m = re.search(r"^expected_derived=([0-9a-f]{64})$", launcher, re.M)
    assert m
    launcher = replace_n(launcher, "expected_derived=" + m.group(1), "expected_derived=" + "0" * 64, 1)
    launcher = successor(launcher)
    launcher = replace_n(launcher, OLD_HEAD, NEW_HEAD, 2)
    launcher = launcher.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    launcher = replace_n(launcher, """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""",
                         """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""", 1)
    env = os.environ.copy()
    env["Q38_A335_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a335-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a335" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp1-4352-ple-only-a226-fullgraphdet-w13n32-client.sh"))
    client = client.replace(OLD_HEAD, NEW_HEAD).replace(OLD_MAP_SHA, NEW_MAP_SHA)
    # A226 is one of the 224 clients pinning a superseded verifier hash; the pin is latent
    # because this record is suite-driven and never runs its client. Pure replay, so no-op.
    if OLD_VERIFIER_SHA in client:
        client = replace_n(client, OLD_VERIFIER_SHA, NEW_VERIFIER_SHA, 1)
    client = replace_n(client, ".m1.w13.BLOCK_SIZE_N == 32", ".m1.w13.BLOCK_SIZE_N == 32", 1)
    supervisor = successor(source("supervise-tp4-mtp1-4352-ple-only-a226-fullgraphdet-w13n32.sh"))
    supervisor = supervisor.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    supervisor = replace_n(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp1-4352-ple-only-a226-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher), 1)
    supervisor = replace_n(supervisor, "expected_client=" + SOURCES["run-tp4-mtp1-4352-ple-only-a226-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client), 1)
    host = successor(source("run-q38-a226-host-controlled.sh"))
    host = replace_n(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp1-4352-ple-only-a226-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor), 1)
    out_names = (
        "launch-tp4-mtp1-4352-ple-only-a335-fullgraphdet-w13n32.sh",
        "run-tp4-mtp1-4352-ple-only-a335-fullgraphdet-w13n32-client.sh",
        "supervise-tp4-mtp1-4352-ple-only-a335-fullgraphdet-w13n32.sh",
        "run-q38-a335-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
