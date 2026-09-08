#!/usr/bin/env python3
"""Create the A324 screen from frozen A305 -- the fused-QSA MTP1 frozen-client record -- with\nthe W13 phase delta neutralised to 64, the change A321 and A322 measured at +0.7 tok/s on\nMTP0.\n\nThe delta resolves only at M=1, and MTP1 verifies at M=2, so it cannot touch the verify\nstep. It can still reach the draft: the speculator is captured separately, runs one token\nper step, and the server captures both [1, 2]. So the expected gain is whatever share of\nthe step the draft head's MoE holds -- real but smaller than MTP0's, and possibly nil if\nthe draft head has no MoE layer of its own.\n\nNo source change: 64 is already an allowed tile, so the head stays the certified 6d872457\nand only the map moves. A305 ran this identical frozen client at 38.981/38.972 (2K) and\n39.299/39.304 (4K) and is the control."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A324_REWRITE_VALIDATE_ONLY") == "1"
SOURCES = {
    'launch-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh': '40abf013e0bed5c8f240bddb4e49df09cef53459fa901ecfddf25846a1d670c3',
    'run-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32-client.sh': '28c5b11cbc75ae39092282e7c6535208391ea68b521f2c02ebe4e0fd72f54ed2',
    'supervise-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh': '0f25f30c1eb401af60630bc48057d00dfd3ff5c40fce00d5f085e339bc677e7b',
    'run-q38-a305-host-controlled.sh': '3406b140c26a0929a4f23242462e85cf9e1539043c5c830d723e3d627e3b0373',
}
HASH_TOKEN = re.compile(r"[0-9a-f]{64}|[0-9a-f]{40}")
OLD_HEAD = "6d8724577dabbee5fa0bbc70c4d927c6174c8d8a"
NEW_HEAD = OLD_HEAD  # no source change: 64 is already an allowed tile
OLD_MAP_SHA = "a8f1f8982e3e1af80ff31b9e0a00afaacf1af1b3c401585109b4d60d3c8267be"
NEW_MAP_SHA = "4fcb5d13ef0c859d12a4fe6b5aac09b04fccf4db24e47a6f004d3f9878e4e38f"
OLD_VERIFIER_SHA = "c874852bbae20f4d738e1f3a37f1b16d553e50dc9e8c56c2b0caabc22675dc0e"
NEW_VERIFIER_SHA = "f7b3e9340e26026ac7998256384ddf7c40ad43a06c1717dc52fba02e284045c9"

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
        seg = seg.replace("tp4-mtp1-4352-ple-only-a305", "tp4-mtp1-4352-ple-only-a324")
        seg = seg.replace("attempt305", "attempt324").replace("19974", "19994")
        seg = seg.replace("ATTEMPT=305", "ATTEMPT=324").replace("a305", "a324").replace("A305", "A324")
        seg = seg.replace("moe-m1-w13-n32", "moe-m1-w13-n64")
        seg = seg.replace("verify-moe-m1-w13-n32-selection", "verify-moe-m1-w13-n64-selection")
        seg = seg.replace("W13-N32", "W13-N64").replace("w13n32", "w13n64")
        return seg
    parts, last = [], 0
    for m in HASH_TOKEN.finditer(text):
        parts.append(rename(text[last:m.start()]))
        parts.append(m.group(0))
        last = m.end()
    parts.append(rename(text[last:]))
    out = "".join(parts)
    assert sorted(HASH_TOKEN.findall(out)) == sorted(HASH_TOKEN.findall(text))
    assert "ATTEMPT=324" in out or "ATTEMPT=" not in out, "the attempt number did not move"
    stripped = HASH_TOKEN.sub("", out)
    assert "19974" not in stripped and "attempt305" not in stripped and "a305" not in stripped
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
                         """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 64""", 1)
    env = os.environ.copy()
    env["Q38_A324_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a324-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a324" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32-client.sh"))
    client = client.replace(OLD_HEAD, NEW_HEAD).replace(OLD_MAP_SHA, NEW_MAP_SHA)
    client = replace_n(client, OLD_VERIFIER_SHA, NEW_VERIFIER_SHA, 1)
    client = replace_n(client, ".m1.w13.BLOCK_SIZE_N == 32", ".m1.w13.BLOCK_SIZE_N == 64", 1)
    supervisor = successor(source("supervise-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh"))
    supervisor = supervisor.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    supervisor = replace_n(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher), 1)
    supervisor = replace_n(supervisor, "expected_client=" + SOURCES["run-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client), 1)
    host = successor(source("run-q38-a305-host-controlled.sh"))
    host = replace_n(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp1-4352-ple-only-a305-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor), 1)
    out_names = (
        "launch-tp4-mtp1-4352-ple-only-a324-fullgraphdet-w13n64.sh",
        "run-tp4-mtp1-4352-ple-only-a324-fullgraphdet-w13n64-client.sh",
        "supervise-tp4-mtp1-4352-ple-only-a324-fullgraphdet-w13n64.sh",
        "run-q38-a324-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
