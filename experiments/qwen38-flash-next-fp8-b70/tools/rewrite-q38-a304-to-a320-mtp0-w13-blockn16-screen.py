#!/usr/bin/env python3
"""Create the A320 screen from frozen A304 -- the fused-QSA MTP0 record packet -- with the
W13 decode GEMM tiled 16 wide in N instead of 32.

MTP0 is where the tile can matter: a phase delta resolves only at M=1, and MTP0 captures
cudagraph_capture_sizes [1]. MTP1 verifies two positions, runs M=2, drops the delta, and
prefers 64 anyway -- A317/A318 spent two runs learning that. At M=1 the W13 GEMM runs
69.1 us per layer at 16 against 77.3 at 32.

A304 ran this same frozen client and is therefore the control: 33.322/33.447 at exact-2K
and 33.471/33.410 at exact-4K, with the same legs in the same order, so no warmup
difference separates them. The tile is exact -- 300 offline cases with zero differing
elements, and both MTP1 server runs returned their lineage hashes -- so A320 must return
afffd2110812 and 1d833e5f4633 unchanged, and its client pins them."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A320_REWRITE_VALIDATE_ONLY") == "1"
SOURCES = {
    'launch-tp4-mtp0-4352-ple-only-a304-fullgraphdet-w13n32.sh': '3b8006ffa6ec7546c2f084039e53a79fbc37a1c35fdfb1365752eeafe090533a',
    'run-tp4-mtp0-4352-ple-only-a304-fullgraphdet-w13n32-client.sh': '54c1f2ecd12f8e6bcc0af7244225a0af4e2dfa4a808a4672dde03bec20e1cee1',
    'supervise-tp4-mtp0-4352-ple-only-a304-fullgraphdet-w13n32.sh': 'd2bd8f4ad7eb047aa87eabd1c32e3242a1aecb640b4d12d915e483f68b1d3ef2',
    'run-q38-a304-host-controlled.sh': '6d8588d6aa058a49d7adfe3f771bf181e827eab2011c155899df263a22eca255',
}
HASH_TOKEN = re.compile(r"[0-9a-f]{64}|[0-9a-f]{40}")
OLD_HEAD = "2a372e860e273273357cb7437ac7de1694304f9f"
NEW_HEAD = "c876369fb2d0f4ed5056786096005da74d1400c2"
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
        seg = seg.replace("tp4-mtp0-4352-ple-only-a304", "tp4-mtp0-4352-ple-only-a320")
        seg = seg.replace("attempt304", "attempt320").replace("19973", "19990")
        seg = seg.replace("ATTEMPT=304", "ATTEMPT=320").replace("a304", "a320").replace("A304", "A320")
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
    assert "19974" not in out and "attempt304" not in out and "a304" not in out
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
    launcher = source("launch-tp4-mtp0-4352-ple-only-a304-fullgraphdet-w13n32.sh")
    m = re.search(r"^expected_derived=([0-9a-f]{64})$", launcher, re.M)
    assert m
    launcher = replace_n(launcher, "expected_derived=" + m.group(1), "expected_derived=" + "0" * 64, 1)
    launcher = successor(launcher)
    launcher = replace_n(launcher, OLD_HEAD, NEW_HEAD, 2)
    launcher = launcher.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    launcher = replace_n(launcher, """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""",
                         """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 16""", 1)
    env = os.environ.copy()
    env["Q38_A320_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a320-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a320" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp0-4352-ple-only-a304-fullgraphdet-w13n32-client.sh"))
    client = client.replace(OLD_HEAD, NEW_HEAD).replace(OLD_MAP_SHA, NEW_MAP_SHA)
    client = replace_n(client, OLD_VERIFIER_SHA, NEW_VERIFIER_SHA, 1)
    client = replace_n(client, ".m1.w13.BLOCK_SIZE_N == 32", ".m1.w13.BLOCK_SIZE_N == 16", 1)
    supervisor = successor(source("supervise-tp4-mtp0-4352-ple-only-a304-fullgraphdet-w13n32.sh"))
    supervisor = supervisor.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    supervisor = replace_n(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp0-4352-ple-only-a304-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher), 1)
    supervisor = replace_n(supervisor, "expected_client=" + SOURCES["run-tp4-mtp0-4352-ple-only-a304-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client), 1)
    host = successor(source("run-q38-a304-host-controlled.sh"))
    host = replace_n(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp0-4352-ple-only-a304-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor), 1)
    out_names = (
        "launch-tp4-mtp0-4352-ple-only-a320-fullgraphdet-w13n16.sh",
        "run-tp4-mtp0-4352-ple-only-a320-fullgraphdet-w13n16-client.sh",
        "supervise-tp4-mtp0-4352-ple-only-a320-fullgraphdet-w13n16.sh",
        "run-q38-a320-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
