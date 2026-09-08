#!/usr/bin/env python3
"""Create the A319 certification packet from frozen A305 — the fused-QSA MTP1 frozen-client
record packet — with the W13 decode GEMM tiled 16 wide in N instead of 32.

A317 screened the tile against the A318 control on the exact-depth driver and returned the
lineage's own hashes, so this is the same identity, not a new one. A319 puts it through the
full client: bench-short, the quality screen, the exact-2K and exact-4K repeats, the
recovery canary, and the official selection receipt — now the W13-N16 verifier, which is the
N32 verifier with the tile constant changed and the widened-allowlist head admitted.

Head a9115342 is the certified overlay 6d872457 plus one line: the per-phase config
validator admits BLOCK_SIZE_N=16, the tile that killed A291 at startup. Nothing else moves,
and with the certified map still selecting 32 no existing run changes behaviour."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A319_REWRITE_VALIDATE_ONLY") == "1"
SOURCES = {
    'launch-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh': '40abf013e0bed5c8f240bddb4e49df09cef53459fa901ecfddf25846a1d670c3',
    'run-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32-client.sh': '28c5b11cbc75ae39092282e7c6535208391ea68b521f2c02ebe4e0fd72f54ed2',
    'supervise-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh': '0f25f30c1eb401af60630bc48057d00dfd3ff5c40fce00d5f085e339bc677e7b',
    'run-q38-a305-host-controlled.sh': '3406b140c26a0929a4f23242462e85cf9e1539043c5c830d723e3d627e3b0373',
}
HASH_TOKEN = re.compile(r"[0-9a-f]{64}|[0-9a-f]{40}")
OLD_HEAD = "6d8724577dabbee5fa0bbc70c4d927c6174c8d8a"
NEW_HEAD = "a911534224263a2ed8a243d266eb5e2b562a3b87"
OLD_MAP_SHA = "a8f1f8982e3e1af80ff31b9e0a00afaacf1af1b3c401585109b4d60d3c8267be"
NEW_MAP_SHA = "89c130d70a34432124b9cee1621080ea75f4b303c20bce784d13af82e4219894"
OLD_VERIFIER_SHA = "c874852bbae20f4d738e1f3a37f1b16d553e50dc9e8c56c2b0caabc22675dc0e"
NEW_VERIFIER_SHA = "9762fe691faa58cac55f9118fe759111c13ad9190a1ea8b320caa526c51d808b"

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
        seg = seg.replace("tp4-mtp1-4352-ple-only-a305", "tp4-mtp1-4352-ple-only-a319")
        seg = seg.replace("attempt305", "attempt319").replace("19974", "19989")
        seg = seg.replace("ATTEMPT=305", "ATTEMPT=319").replace("a305", "a319").replace("A305", "A319")
        seg = seg.replace("moe-m1-w13-n32", "moe-m1-w13-n16")
        seg = seg.replace("verify-moe-m1-w13-n32-selection", "verify-moe-m1-w13-n16-selection")
        seg = seg.replace("W13-N32", "W13-N16").replace("w13n32", "w13n16")
        return seg
    parts, last = [], 0
    for m in HASH_TOKEN.finditer(text):
        parts.append(rename(text[last:m.start()]))
        parts.append(m.group(0))
        last = m.end()
    parts.append(rename(text[last:]))
    out = "".join(parts)
    assert sorted(HASH_TOKEN.findall(out)) == sorted(HASH_TOKEN.findall(text))
    assert "19974" not in out and "attempt305" not in out and "a305" not in out
    assert "moe-m1-w13-n32" not in out and "w13n32" not in out and "W13-N32" not in out
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
    launcher = source("launch-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh")
    m = re.search(r"^expected_derived=([0-9a-f]{64})$", launcher, re.M)
    assert m
    launcher = replace_n(launcher, "expected_derived=" + m.group(1), "expected_derived=" + "0" * 64, 1)
    launcher = successor(launcher)
    launcher = replace_n(launcher, OLD_HEAD, NEW_HEAD, 2)
    launcher = launcher.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    launcher = replace_n(launcher, """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""",
                         """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 16""", 1)
    env = os.environ.copy()
    env["Q38_A319_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a319-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a319" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32-client.sh"))
    client = client.replace(OLD_HEAD, NEW_HEAD).replace(OLD_MAP_SHA, NEW_MAP_SHA)
    client = replace_n(client, OLD_VERIFIER_SHA, NEW_VERIFIER_SHA, 1)
    client = replace_n(client, ".m1.w13.BLOCK_SIZE_N == 32", ".m1.w13.BLOCK_SIZE_N == 16", 1)
    supervisor = successor(source("supervise-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh"))
    supervisor = supervisor.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    supervisor = replace_n(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher), 1)
    supervisor = replace_n(supervisor, "expected_client=" + SOURCES["run-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client), 1)
    host = successor(source("run-q38-a305-host-controlled.sh"))
    host = replace_n(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor), 1)
    out_names = (
        "launch-tp4-mtp1-4352-ple-only-a319-fullgraphdet-w13n16.sh",
        "run-tp4-mtp1-4352-ple-only-a319-fullgraphdet-w13n16-client.sh",
        "supervise-tp4-mtp1-4352-ple-only-a319-fullgraphdet-w13n16.sh",
        "run-q38-a319-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
