#!/usr/bin/env python3
"""Create the A339 fourth suite on the Triton-HC overlay 62219122.\n\nA338 gave fused-QSA a fourth suite and it landed lowest of the four, breaking the\nno-overlap result the three-against-three comparison had shown and dropping the gap of\nmeans from +0.60 to +0.42. That comparison is now four samples against three, and an\nunequal-n range comparison is exactly what I warned about earlier: it flatters whichever\narm has fewer draws. This equalises it at four each, which is the minimum for the\ncomparison to be fair, though not enough to pin the gap."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A339_REWRITE_VALIDATE_ONLY") == "1"
SOURCES = {
    'launch-tp4-mtp1-4352-ple-only-a272-fullgraphdet-w13n32.sh': '73db4a9b4893103728574105882d0eaec33ae368fc5fa7c8363ce9a6563a64af',
    'run-tp4-mtp1-4352-ple-only-a272-fullgraphdet-w13n32-client.sh': 'b18b42f4e1c9528f849a522d325bc750205beb4d6795e0dc10dab9584207ba97',
    'supervise-tp4-mtp1-4352-ple-only-a272-fullgraphdet-w13n32.sh': '389cfe5f8d31b55dfb030d2b26e80d624003b1468424eb10ec93bd028aeaeaa9',
    'run-q38-a272-host-controlled.sh': '5375628b42a3b592d3bb81463d7ad5d7367e1e1b4d00dbb086f3faf7990de82d',
}
HASH_TOKEN = re.compile(r"[0-9a-f]{64}|[0-9a-f]{40}")
OLD_HEAD = "622191221475b53cc6f7f4d847860939f4c300ab"
NEW_HEAD = OLD_HEAD  # no source change: 64 is already an allowed tile
OLD_MAP_SHA = "a8f1f8982e3e1af80ff31b9e0a00afaacf1af1b3c401585109b4d60d3c8267be"
NEW_MAP_SHA = OLD_MAP_SHA  # pure replay: the certified map is unchanged
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
        seg = seg.replace("tp4-mtp1-4352-ple-only-a272", "tp4-mtp1-4352-ple-only-a339")
        seg = seg.replace("attempt272", "attempt339").replace("19942", "19952")
        seg = seg.replace("ATTEMPT=272", "ATTEMPT=339").replace("a272", "a339").replace("A272", "A339")
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
    assert "ATTEMPT=339" in out or "ATTEMPT=" not in out, "the attempt number did not move"
    assert "19974" not in out and "attempt272" not in out and "a272" not in out
    # A pure replay keeps the certified map, so the map name is expected to survive.
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
    launcher = source("launch-tp4-mtp1-4352-ple-only-a272-fullgraphdet-w13n32.sh")
    m = re.search(r"^expected_derived=([0-9a-f]{64})$", launcher, re.M)
    assert m
    launcher = replace_n(launcher, "expected_derived=" + m.group(1), "expected_derived=" + "0" * 64, 1)
    launcher = successor(launcher)
    launcher = replace_n(launcher, OLD_HEAD, NEW_HEAD, 2)
    launcher = launcher.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    launcher = replace_n(launcher, """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""",
                         """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""", 1)
    env = os.environ.copy()
    env["Q38_A339_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a339-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a339" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp1-4352-ple-only-a272-fullgraphdet-w13n32-client.sh"))
    client = client.replace(OLD_HEAD, NEW_HEAD).replace(OLD_MAP_SHA, NEW_MAP_SHA)
    # Pure replay: the verifier is unchanged, so this is a no-op. A272 pins a superseded
    # verifier sha (20546ff1, against today's c874852b) and never ran its client, so the
    # pin is latent; the replay is suite-driven and does not touch it.
    if OLD_VERIFIER_SHA in client:
        client = replace_n(client, OLD_VERIFIER_SHA, NEW_VERIFIER_SHA, 1)
    client = replace_n(client, ".m1.w13.BLOCK_SIZE_N == 32", ".m1.w13.BLOCK_SIZE_N == 32", 1)
    supervisor = successor(source("supervise-tp4-mtp1-4352-ple-only-a272-fullgraphdet-w13n32.sh"))
    supervisor = supervisor.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    supervisor = replace_n(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp1-4352-ple-only-a272-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher), 1)
    supervisor = replace_n(supervisor, "expected_client=" + SOURCES["run-tp4-mtp1-4352-ple-only-a272-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client), 1)
    host = successor(source("run-q38-a272-host-controlled.sh"))
    host = replace_n(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp1-4352-ple-only-a272-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor), 1)
    out_names = (
        "launch-tp4-mtp1-4352-ple-only-a339-fullgraphdet-w13n32.sh",
        "run-tp4-mtp1-4352-ple-only-a339-fullgraphdet-w13n32-client.sh",
        "supervise-tp4-mtp1-4352-ple-only-a339-fullgraphdet-w13n32.sh",
        "run-q38-a339-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
