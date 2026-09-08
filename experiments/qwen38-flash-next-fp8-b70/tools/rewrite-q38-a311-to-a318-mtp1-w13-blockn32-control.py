#!/usr/bin/env python3
"""Create the A318 control from frozen A311: the N=32 counterpart of the A317 screen.

A305 measured the certified W13-N32 tile at 38.981/38.972 (2K), but through the frozen
client, whose bench-short and quality legs warm the server first. The exact-depth driver
runs its rows cold, and driver-only attempts on this lineage land near 37 on the second
row, so comparing A317's driver rows against A305's client rows would credit the tile
with a warmup difference. A318 is the control: the same driver, the same head, the same
everything, with the certified 32-wide map instead of the 16-wide one.

Head 6d872457 is the certified fused-QSA MTP1 overlay. A317's head is exactly this plus
the one-line allowlist widening, which cannot matter when the map selects 32."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A318_REWRITE_VALIDATE_ONLY") == "1"
SOURCES = {
    'launch-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh': '08bf8ff673036d25028e5d9d1d30a5d0fe919d27f4988b864cb4b0e197422d73',
    'run-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32-client.sh': '4c442ccbd036a0f20cf5464192fd0a3f89fdb73466d2e58f95e3272a611eca49',
    'supervise-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh': 'c8cbd49bf9530dbb6394552f4d8784fb2955bd1d5f91efad73da64a05bce8f58',
    'run-q38-a311-host-controlled.sh': 'db778ea52d75ab467e807ecd3a0433f0bcacdbd02fef8325eeb828e14f5f6408',
}
HASH_TOKEN = re.compile(r"[0-9a-f]{64}|[0-9a-f]{40}")
OLD_HEAD = "795a9dd94c16bcfbedc2117bbcb33c988f2e6c90"
NEW_HEAD = "6d8724577dabbee5fa0bbc70c4d927c6174c8d8a"  # the certified fused-QSA MTP1 overlay, unmodified
OLD_MAP_SHA = "a8f1f8982e3e1af80ff31b9e0a00afaacf1af1b3c401585109b4d60d3c8267be"
NEW_MAP_SHA = OLD_MAP_SHA  # the control keeps the certified map

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
        seg = seg.replace("tp4-mtp1-4352-ple-only-a311", "tp4-mtp1-4352-ple-only-a318")
        seg = seg.replace("attempt311", "attempt318").replace("19979", "19988")
        seg = seg.replace("ATTEMPT=311", "ATTEMPT=318").replace("a311", "a318").replace("A311", "A318")
        return seg
    parts, last = [], 0
    for m in HASH_TOKEN.finditer(text):
        parts.append(rename(text[last:m.start()]))
        parts.append(m.group(0))
        last = m.end()
    parts.append(rename(text[last:]))
    out = "".join(parts)
    assert sorted(HASH_TOKEN.findall(out)) == sorted(HASH_TOKEN.findall(text))
    assert "19979" not in out and "attempt311" not in out and "a311" not in out
    return out

def replace_n(t, a, b, n):
    assert t.count(a) == n, (t.count(a), a[:80])
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
    launcher = source("launch-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh")
    m = re.search(r"^expected_derived=([0-9a-f]{64})$", launcher, re.M)
    assert m
    launcher = replace_n(launcher, "expected_derived=" + m.group(1), "expected_derived=" + "0" * 64, 1)
    launcher = successor(launcher)
    launcher = replace_n(launcher, OLD_HEAD, NEW_HEAD, 2)
    launcher = launcher.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    # The census hook does not exist on this head; drop its switch so the identity is clean.
    launcher = replace_n(launcher, "export Q38_PLACEMENT_HIT_CENSUS=1\n", "", 1)
    env = os.environ.copy()
    env["Q38_A318_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a318-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a318" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32-client.sh"))
    client = client.replace(OLD_HEAD, NEW_HEAD).replace(OLD_MAP_SHA, NEW_MAP_SHA)
    supervisor = successor(source("supervise-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh"))
    supervisor = supervisor.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    supervisor = replace_n(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher), 1)
    supervisor = replace_n(supervisor, "expected_client=" + SOURCES["run-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client), 1)
    host = successor(source("run-q38-a311-host-controlled.sh"))
    host = replace_n(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor), 1)
    out_names = (
        "launch-tp4-mtp1-4352-ple-only-a318-fullgraphdet-w13n32.sh",
        "run-tp4-mtp1-4352-ple-only-a318-fullgraphdet-w13n32-client.sh",
        "supervise-tp4-mtp1-4352-ple-only-a318-fullgraphdet-w13n32.sh",
        "run-q38-a318-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
