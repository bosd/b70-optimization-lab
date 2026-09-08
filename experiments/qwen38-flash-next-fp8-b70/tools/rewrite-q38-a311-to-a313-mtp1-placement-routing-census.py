#!/usr/bin/env python3
"""Create the A313 packet from frozen A311: the same fused-QSA MTP1 identity and the same
3.5 GiB-per-rank expert host placement, with a full per-expert routing census on head
c3b044c1 (per-rank JSON via Q38_PLACEMENT_HIT_CENSUS_OUT). A311 proved parked experts are
selected (1.0-1.1% of routed blocks on three ranks, 17.5% on the rank holding the hot
experts), so the 2026-09-06 never-hit survey is stale for this lineage; this run measures
the lineage's own routing histogram, which the placement builder consumes to park the
coldest experts by current evidence. Diagnostic: the census hook adds device work, so its
rate is not a speed measurement."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A313_REWRITE_VALIDATE_ONLY") == "1"
SOURCES = {
    'launch-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh': '08bf8ff673036d25028e5d9d1d30a5d0fe919d27f4988b864cb4b0e197422d73',
    'run-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32-client.sh': '4c442ccbd036a0f20cf5464192fd0a3f89fdb73466d2e58f95e3272a611eca49',
    'supervise-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh': 'c8cbd49bf9530dbb6394552f4d8784fb2955bd1d5f91efad73da64a05bce8f58',
    'run-q38-a311-host-controlled.sh': 'db778ea52d75ab467e807ecd3a0433f0bcacdbd02fef8325eeb828e14f5f6408',
}
HASH_TOKEN = re.compile(r"[0-9a-f]{64}|[0-9a-f]{40}")
OLD_HEAD = "795a9dd94c16bcfbedc2117bbcb33c988f2e6c90"
NEW_HEAD = "c3b044c11d84ed9ea35b01aa06b3deefff0a0fff"  # q38-placement-hit-census-v2: full per-expert routing histogram + per-rank dump
CENSUS_OUT = "/tmp/q38-a313-census"

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
        seg = seg.replace("tp4-mtp1-4352-ple-only-a311", "tp4-mtp1-4352-ple-only-a313")
        seg = seg.replace("attempt311", "attempt313").replace("19979", "19983")
        seg = seg.replace("ATTEMPT=311", "ATTEMPT=313").replace("a311", "a313").replace("A311", "A313")
        return seg
    parts = []
    last = 0
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

def replace_once(t, a, b):
    return replace_n(t, a, b, 1)

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
    launcher = replace_once(launcher, "expected_derived=" + m.group(1), "expected_derived=" + "0" * 64)
    launcher = successor(launcher)
    launcher = replace_n(launcher, OLD_HEAD, NEW_HEAD, 2)
    # The census writes one JSON per rank naming the host-placed experts it saw selected.
    launcher = replace_once(
        launcher,
        "\nexport Q38_EXPERT_HOST_PLACEMENT=",
        "\nexport Q38_PLACEMENT_HIT_CENSUS_OUT=" + CENSUS_OUT + "\nexport Q38_EXPERT_HOST_PLACEMENT=",
    )
    env = os.environ.copy()
    env["Q38_A313_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a313-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a313" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32-client.sh"))
    client = client.replace(OLD_HEAD, NEW_HEAD)
    assert NEW_HEAD in client and OLD_HEAD not in client
    supervisor = successor(source("supervise-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh"))
    supervisor = replace_once(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher))
    supervisor = replace_once(supervisor, "expected_client=" + SOURCES["run-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client))
    host = successor(source("run-q38-a311-host-controlled.sh"))
    host = replace_once(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp1-4352-ple-only-a311-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor))
    out_names = (
        "launch-tp4-mtp1-4352-ple-only-a313-fullgraphdet-w13n32.sh",
        "run-tp4-mtp1-4352-ple-only-a313-fullgraphdet-w13n32-client.sh",
        "supervise-tp4-mtp1-4352-ple-only-a313-fullgraphdet-w13n32.sh",
        "run-q38-a313-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
