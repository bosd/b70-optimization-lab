#!/usr/bin/env python3
"""Create the A314 packet from frozen A306 — the certified fused-QSA MTP1 record packet —
changing exactly one thing: the expert host placement file. A306 loads the 2026-09-06
never-hit survey taken on the torch-fallback line; A311 showed that survey is stale here
(1.0-1.1% of routed blocks on three ranks select a parked expert, 17.5% on the rank holding
the hot experts, each a PCIe read of a whole expert row). A314 loads the placement rebuilt
from A313's routing census of this lineage, under the same 3.5 GiB-per-rank budget and the
same never-selected policy.

Everything else — head, kernels, selectors, offload, tuned map, the realistic-suite client
and its gates — is A306's, so the comparison against the certified 38.97 tok/s record is
single-variable. Which memory a weight lives in does not touch the arithmetic, so the
exact-2K and exact-4K hashes must not move; the client's pins enforce that."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A314_REWRITE_VALIDATE_ONLY") == "1"
SOURCES = {
    'launch-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh': '147448971cddd7147e77e5b1d35b8bb077f717890dc5d6a93525e66db81ce3d3',
    'run-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32-client.sh': '8c568d14dfba07cb1829d0e3c385a4a189bcaef3b4bfa6073bc1d4d5d1725bf1',
    'supervise-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh': '905d8a8f09e6ca93712f07dbb35345b6732865c0d848e36e2fb4315efaa87977',
    'run-q38-a306-host-controlled.sh': 'ba38941bc835e68a8cbd89a21ed562d9dcdf6a0e2b055fb7dc92fbe23d2139d4',
}
HASH_TOKEN = re.compile(r"[0-9a-f]{64}|[0-9a-f]{40}")
OLD_PLACEMENT = "/home/steve/llm-optimizations/experiments/qwen38-flash-next-fp8-b70/data/20260906-q38-expert-host-placement-3p5gib-per-rank.json"
NEW_PLACEMENT = "/home/steve/llm-optimizations/experiments/qwen38-flash-next-fp8-b70/data/20260907-q38-expert-host-placement-fusedqsa-census-3p5gib-per-rank.json"

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
        seg = seg.replace("tp4-mtp1-4352-ple-only-a306", "tp4-mtp1-4352-ple-only-a314")
        seg = seg.replace("attempt306", "attempt314").replace("19975", "19984")
        seg = seg.replace("ATTEMPT=306", "ATTEMPT=314").replace("a306", "a314").replace("A306", "A314")
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
    assert "19975" not in out and "attempt306" not in out and "a306" not in out
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
    assert Path(NEW_PLACEMENT).is_file(), f"build the census placement first: {NEW_PLACEMENT}"
    launcher = source("launch-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh")
    m = re.search(r"^expected_derived=([0-9a-f]{64})$", launcher, re.M)
    assert m
    launcher = replace_n(launcher, "expected_derived=" + m.group(1), "expected_derived=" + "0" * 64, 1)
    launcher = successor(launcher)
    launcher = replace_n(launcher, OLD_PLACEMENT, NEW_PLACEMENT, 1)
    env = os.environ.copy()
    env["Q38_A314_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a314-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a314" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32-client.sh"))
    # The recorded identity must name the placement the run actually loads.
    client = replace_n(client, OLD_PLACEMENT, NEW_PLACEMENT, 1)
    supervisor = successor(source("supervise-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh"))
    supervisor = replace_n(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher), 1)
    supervisor = replace_n(supervisor, "expected_client=" + SOURCES["run-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client), 1)
    host = successor(source("run-q38-a306-host-controlled.sh"))
    host = replace_n(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor), 1)
    out_names = (
        "launch-tp4-mtp1-4352-ple-only-a314-fullgraphdet-w13n32.sh",
        "run-tp4-mtp1-4352-ple-only-a314-fullgraphdet-w13n32-client.sh",
        "supervise-tp4-mtp1-4352-ple-only-a314-fullgraphdet-w13n32.sh",
        "run-q38-a314-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
