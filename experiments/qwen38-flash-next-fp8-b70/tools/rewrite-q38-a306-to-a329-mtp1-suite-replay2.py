#!/usr/bin/env python3
"""Create the A329 second replay of A306, identical to A328 but for attempt and port.\n\nA328 reproduced the certified lossless-MTP1 record within 0.54%, with the shortfall\nconcentrated in the first two rows of a cold run. One pair cannot separate that lane's\nsuite-to-suite spread from a real shift, and MTP1 is the noisier of the two lineages\nbecause speculation acceptance varies run to run. A second replay makes the spread a\nmeasurement rather than an inference, which every future MTP1 record comparison needs."""
from __future__ import annotations
import hashlib, os, re, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VALIDATE_ONLY = os.environ.get("Q38_A329_REWRITE_VALIDATE_ONLY") == "1"
SOURCES = {
    'launch-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh': '147448971cddd7147e77e5b1d35b8bb077f717890dc5d6a93525e66db81ce3d3',
    'run-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32-client.sh': '8c568d14dfba07cb1829d0e3c385a4a189bcaef3b4bfa6073bc1d4d5d1725bf1',
    'supervise-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh': '905d8a8f09e6ca93712f07dbb35345b6732865c0d848e36e2fb4315efaa87977',
    'run-q38-a306-host-controlled.sh': 'ba38941bc835e68a8cbd89a21ed562d9dcdf6a0e2b055fb7dc92fbe23d2139d4',
}
HASH_TOKEN = re.compile(r"[0-9a-f]{64}|[0-9a-f]{40}")
OLD_HEAD = "6d8724577dabbee5fa0bbc70c4d927c6174c8d8a"
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
        seg = seg.replace("tp4-mtp1-4352-ple-only-a306", "tp4-mtp1-4352-ple-only-a329")
        seg = seg.replace("attempt306", "attempt329").replace("19975", "19999")
        seg = seg.replace("ATTEMPT=306", "ATTEMPT=329").replace("a306", "a329").replace("A306", "A329")
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
    assert "ATTEMPT=329" in out or "ATTEMPT=" not in out, "the attempt number did not move"
    assert "19974" not in out and "attempt306" not in out and "a306" not in out
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
    launcher = source("launch-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh")
    m = re.search(r"^expected_derived=([0-9a-f]{64})$", launcher, re.M)
    assert m
    launcher = replace_n(launcher, "expected_derived=" + m.group(1), "expected_derived=" + "0" * 64, 1)
    launcher = successor(launcher)
    launcher = replace_n(launcher, OLD_HEAD, NEW_HEAD, 2)
    launcher = launcher.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    launcher = replace_n(launcher, """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""",
                         """.W1_CONFIG.BLOCK_SIZE_N' "$tuned_config_map")" == 32""", 1)
    env = os.environ.copy()
    env["Q38_A329_DERIVED_SOURCE_ONLY"] = "1"
    derived = subprocess.run(["bash"], input=launcher, text=True, capture_output=True, check=True, env=env).stdout
    Path("/tmp/q38-ple2k-a329-base.sh").unlink(missing_ok=True)
    assert "q38-ple2k-a329" in derived
    launcher = launcher.replace("expected_derived=" + "0" * 64, "expected_derived=" + digest(derived))
    client = successor(source("run-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32-client.sh"))
    client = client.replace(OLD_HEAD, NEW_HEAD).replace(OLD_MAP_SHA, NEW_MAP_SHA)
    client = replace_n(client, OLD_VERIFIER_SHA, NEW_VERIFIER_SHA, 1)
    client = replace_n(client, ".m1.w13.BLOCK_SIZE_N == 32", ".m1.w13.BLOCK_SIZE_N == 32", 1)
    supervisor = successor(source("supervise-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh"))
    supervisor = supervisor.replace(OLD_MAP_SHA, NEW_MAP_SHA)
    supervisor = replace_n(supervisor, "expected_wrapper=" + SOURCES["launch-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh"], "expected_wrapper=" + digest(launcher), 1)
    supervisor = replace_n(supervisor, "expected_client=" + SOURCES["run-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32-client.sh"], "expected_client=" + digest(client), 1)
    host = successor(source("run-q38-a306-host-controlled.sh"))
    host = replace_n(host, "expected_supervisor=" + SOURCES["supervise-tp4-mtp1-4352-ple-only-a306-fullgraphdet-w13n32.sh"], "expected_supervisor=" + digest(supervisor), 1)
    out_names = (
        "launch-tp4-mtp1-4352-ple-only-a329-fullgraphdet-w13n32.sh",
        "run-tp4-mtp1-4352-ple-only-a329-fullgraphdet-w13n32-client.sh",
        "supervise-tp4-mtp1-4352-ple-only-a329-fullgraphdet-w13n32.sh",
        "run-q38-a329-host-controlled.sh",
    )
    for name, text in zip(out_names, (launcher, client, supervisor, host)):
        emit(name, text)
    for name in out_names:
        print(digest((ROOT / name).read_bytes()), name)

if __name__ == "__main__":
    main()
