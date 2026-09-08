#!/usr/bin/env python3
"""Create the A325 suite run from frozen A301, the packet behind the published MTP0 figure of\n33.797067 tok/s, with the W13 phase delta neutralised to 64.\n\nA323 was the same packet run through the frozen client, and it failed after every leg on a\nstale hash pin: A301's client pins the torch-fallback exact-4K authority c6193cc6 while\nthis lineage produces 1d833e5f. That pin had never been exercised, because A301 itself ran\nonly the suite leg -- its run directory holds the suite result and nothing else. A325\ntherefore runs the suite driver, which is how the published number was produced, so the\nmedians are comparable and the unexercised client pin stays out of the way.\n\nA323 is not wasted: its exact rows came back at 34.167/34.150 (2K) and 34.089/34.110 (4K)\nwith the lineage hashes, a third independent confirmation of the +0.7 tok/s after A321 and\nA322.\n\nNo source change: 64 is already an allowed tile, so the head stays the certified 2a372e86."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A325_REWRITE_VALIDATE_ONLY") == "1"
SOURCES = {
    'launch-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32.sh': 'c6b95a4c751ea54c65abe375c8d5fc14ffedccd3a85bbb05afab4eca2b9d4bcc',
    'run-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32-client.sh': 'a9c0e2ea181af95c14be509da038fc924e887ccfddb48e2f8b411802e3d0f404',
    'supervise-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32.sh': '2440ebb811701c90c7a8398fb4492ba8bdfdc466c6ecb5a3fa9851a35de682e7',
    'run-q38-a301-host-controlled.sh': '394cb616de2d4943b9d55344b11a8a3a9fda6b94fcfcbbfb8d6b9faa72688338',
}
HASH_TOKEN = re.compile(r"[0-9a-f]{64}|[0-9a-f]{40}")
OLD_HEAD = "2a372e860e273273357cb7437ac7de1694304f9f"
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
        seg = seg.replace("tp4-mtp0-4352-ple-only-a301", "tp4-mtp0-4352-ple-only-a325")
        seg = seg.replace("attempt301", "attempt325").replace("19970", "19995")
        seg = seg.replace("ATTEMPT=301", "ATTEMPT=325").replace("a301", "a325").replace("A301", "A325")
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
    # Check the renamed text only: a sha256 token can contain the digits of the old port,
    # and rename deliberately does not touch hashes.
    stripped = HASH_TOKEN.sub("", out)
    assert "19970" not in stripped and "attempt301" not in stripped and "a301" not in stripped
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
    launcher = source("launch-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32.sh")
    m = re.search(r"^expected_derived=([0-9a-f]{64})$", launcher, re.M)
    assert m
    launcher = replace_n(launcher, "expected_derived=" + m.group(1), "expected_derived=" + "0" * 64, 1)
    launcher = successor(launcher)
    launcher = replace_n(launcher, OLD_HEAD, NEW_HEAD, 2)
    launcher = launcher.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    launcher = replace_n(launcher, """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""",
                         """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 64""", 1)
    env = os.environ.copy()
    env["Q38_A325_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a325-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a325" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32-client.sh"))
    client = client.replace(OLD_HEAD, NEW_HEAD).replace(OLD_MAP_SHA, NEW_MAP_SHA)
    client = replace_n(client, OLD_VERIFIER_SHA, NEW_VERIFIER_SHA, 1)
    client = replace_n(client, ".m1.w13.BLOCK_SIZE_N == 32", ".m1.w13.BLOCK_SIZE_N == 64", 1)
    supervisor = successor(source("supervise-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32.sh"))
    supervisor = supervisor.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    supervisor = replace_n(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher), 1)
    supervisor = replace_n(supervisor, "expected_client=" + SOURCES["run-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client), 1)
    host = successor(source("run-q38-a301-host-controlled.sh"))
    host = replace_n(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor), 1)
    out_names = (
        "launch-tp4-mtp0-4352-ple-only-a325-fullgraphdet-w13n64.sh",
        "run-tp4-mtp0-4352-ple-only-a325-fullgraphdet-w13n64-client.sh",
        "supervise-tp4-mtp0-4352-ple-only-a325-fullgraphdet-w13n64.sh",
        "run-q38-a325-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
