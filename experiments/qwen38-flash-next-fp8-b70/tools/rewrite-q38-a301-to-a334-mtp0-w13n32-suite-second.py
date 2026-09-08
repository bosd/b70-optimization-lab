#!/usr/bin/env python3
"""Create the A334 second suite on the *superseded* MTP0 W13-N32 line (A301's configuration).\n\nThe promotion is currently three suites on the new line against one on the old: 34.4953 /\n34.5101 / 34.5201 versus 33.797067. That is a 28x separation and is not in doubt, but it is\na distribution compared against a single point. Building the superseded side out lets the\npromotion be stated as distribution against distribution, and gives the W13-N32 line the\nsame error bars its successor now has.\n\nPure replay of A301: certified map, certified verifier, head 2a372e86, nothing changed but\nattempt and port."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A334_REWRITE_VALIDATE_ONLY") == "1"
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
        seg = seg.replace("tp4-mtp0-4352-ple-only-a301", "tp4-mtp0-4352-ple-only-a334")
        seg = seg.replace("attempt301", "attempt334").replace("19970", "19947")
        seg = seg.replace("ATTEMPT=301", "ATTEMPT=334").replace("a301", "a334").replace("A301", "A334")
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
    assert "ATTEMPT=334" in out or "ATTEMPT=" not in out, "the attempt number did not move"
    # Check the renamed text only: a sha256 token can contain the digits of the old port,
    # and rename deliberately does not touch hashes.
    stripped = HASH_TOKEN.sub("", out)
    assert "19970" not in stripped and "attempt301" not in stripped and "a301" not in stripped
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
    launcher = source("launch-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32.sh")
    m = re.search(r"^expected_derived=([0-9a-f]{64})$", launcher, re.M)
    assert m
    launcher = replace_n(launcher, "expected_derived=" + m.group(1), "expected_derived=" + "0" * 64, 1)
    launcher = successor(launcher)
    launcher = replace_n(launcher, OLD_HEAD, NEW_HEAD, 2)
    launcher = launcher.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    launcher = replace_n(launcher, """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""",
                         """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""", 1)
    env = os.environ.copy()
    env["Q38_A334_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a334-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a334" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32-client.sh"))
    client = client.replace(OLD_HEAD, NEW_HEAD).replace(OLD_MAP_SHA, NEW_MAP_SHA)
    client = replace_n(client, OLD_VERIFIER_SHA, NEW_VERIFIER_SHA, 1)
    client = replace_n(client, ".m1.w13.BLOCK_SIZE_N == 32", ".m1.w13.BLOCK_SIZE_N == 32", 1)
    supervisor = successor(source("supervise-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32.sh"))
    supervisor = supervisor.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    supervisor = replace_n(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher), 1)
    supervisor = replace_n(supervisor, "expected_client=" + SOURCES["run-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client), 1)
    host = successor(source("run-q38-a301-host-controlled.sh"))
    host = replace_n(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp0-4352-ple-only-a301-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor), 1)
    out_names = (
        "launch-tp4-mtp0-4352-ple-only-a334-fullgraphdet-w13n32.sh",
        "run-tp4-mtp0-4352-ple-only-a334-fullgraphdet-w13n32-client.sh",
        "supervise-tp4-mtp0-4352-ple-only-a334-fullgraphdet-w13n32.sh",
        "run-q38-a334-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
