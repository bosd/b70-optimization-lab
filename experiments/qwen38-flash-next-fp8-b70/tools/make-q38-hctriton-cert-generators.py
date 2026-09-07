#!/usr/bin/env python3
"""Derive the Triton-HC new-authority certification generators (A269 MTP0 battery, A270 MTP0 suite,
A271 MTP1 battery, A272 MTP1 suite) from the certified placement generators (A223 / A227 / A225 / A226):
HC-only heads 8d7d6fd8 (MTP0) / 62219122 (MTP1) = certified placement heads + 7751df34, VLLM_XPU_HC_TRITON=1
printed into the derived source (wrapper-level VLLM_* exports are stripped), identity literal
…_placement_hctriton, the current verifier pin, and the frozen client's exact-depth authority literals
repinned to the new 2K/4K hashes established by the A266/A267 fresh-server pair (MTP1 hashes default to
the MTP0 ones: lossless MTP1 must reproduce them). Split-K is excluded: it changes outputs at 4K (A259).

  make-q38-hctriton-cert-generators.py --hash2k <sha256> --hash4k <sha256> [--mtp1-hash2k …] [--mtp1-hash4k …]
"""
import argparse, hashlib, re
from pathlib import Path
T = Path(__file__).resolve().parent
HASH = re.compile(r'[0-9a-f]{12,}')
OLD2K = 'afffd2110812762164862b6388f054bb56696ee57b07eadce411a702c40bc714'
OLD4K = 'c6193cc6c9a1553f56d7ce78faea9c8bfa628a67fcea229b1c99279a149f6639'
OLD_VERIFIER = '13073e712ba4743cd0da1d43e4eddc4d7a246b5eda28cdff0ba9f9999243cef0'
PLAN = [  # (src gen, dst gen, old attempt, new attempt, old port, new port, head swap, mtp1?)
    ('rewrite-q38-a78-to-a223-placement-ple-embed-frozen-client.py', 'rewrite-q38-a78-to-a269-placement-hctriton-frozen-client.py', 223, 269, '19893', '19939', ('cb59004b5c51e603ba06579382e66139d9a18bb6', '8d7d6fd8e392da59e2f516870e5f4fc76d4ca230'), False),
    ('rewrite-q38-a78-to-a227-placement-ple-embed-realistic-suite.py', 'rewrite-q38-a78-to-a270-placement-hctriton-realistic-suite.py', 227, 270, '19897', '19940', ('cb59004b5c51e603ba06579382e66139d9a18bb6', '8d7d6fd8e392da59e2f516870e5f4fc76d4ca230'), False),
    ('rewrite-q38-a120-to-a225-mtp1-placement-ple-embed-frozen-client.py', 'rewrite-q38-a120-to-a271-mtp1-placement-hctriton-frozen-client.py', 225, 271, '19895', '19941', ('005dc57895896f770157ea94f68e473e7447139e', '622191221475b53cc6f7f4d847860939f4c300ab'), True),
    ('rewrite-q38-a120-to-a226-mtp1-placement-ple-embed-realistic-suite.py', 'rewrite-q38-a120-to-a272-mtp1-placement-hctriton-realistic-suite.py', 226, 272, '19896', '19942', ('005dc57895896f770157ea94f68e473e7447139e', '622191221475b53cc6f7f4d847860939f4c300ab'), True),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hash2k', required=True); ap.add_argument('--hash4k', required=True)
    ap.add_argument('--mtp1-hash2k'); ap.add_argument('--mtp1-hash4k')
    a = ap.parse_args()
    for h in (a.hash2k, a.hash4k, a.mtp1_hash2k or a.hash2k, a.mtp1_hash4k or a.hash4k):
        assert re.fullmatch(r'[0-9a-f]{64}', h), h
    verifier = hashlib.sha256((T / 'verify-moe-m1-w13-n32-selection.py').read_bytes()).hexdigest()
    for src, dst, o, n, oport, nport, (oh, nh), mtp1 in PLAN:
        h2k = (a.mtp1_hash2k or a.hash2k) if mtp1 else a.hash2k
        h4k = (a.mtp1_hash4k or a.hash4k) if mtp1 else a.hash4k
        s = (T / src).read_text()
        def sub(seg):
            return (seg.replace(f'a{o}', f'a{n}').replace(f'A{o}', f'A{n}').replace(f'attempt{o}', f'attempt{n}')
                    .replace(f'ATTEMPT={o}', f'ATTEMPT={n}').replace(oport, nport))
        out, pos = [], 0
        for m in HASH.finditer(s):
            out.append(sub(s[pos:m.start()])); h = m.group(0)
            if h == oh: h = nh
            elif h == oh[:12]: h = nh[:12]
            elif h == OLD_VERIFIER: h = verifier
            out.append(h); pos = m.end()
        out.append(sub(s[pos:])); s2 = ''.join(out)
        key = 'ple_embed_budget12p25_uva_cold_expert_host_placement'
        assert s2.count(key) == 1, (src, key); s2 = s2.replace(key, key + '_hctriton')
        key = '    launcher = replace_n(launcher, OLD_HEAD, NEW_HEAD, 2)\n'
        assert s2.count(key) == 1, (src, key)
        s2 = s2.replace(key, key + '    launcher = replace_once(launcher, \'  print "export VLLM_XPU_MKLDNN_DETERMINISTIC=1"\\n\', \'  print "export VLLM_XPU_MKLDNN_DETERMINISTIC=1"\\n  print "export VLLM_XPU_HC_TRITON=1"\\n\')  # Triton HC glue in the derived source (wrapper-level VLLM_* exports are stripped)\n')
        key = '    client = client.replace(OLD_HEAD, NEW_HEAD)\n'
        assert s2.count(key) == 1, (src, key)
        s2 = s2.replace(key, key +
            f'    assert client.count("{OLD2K}") == 1 and client.count("{OLD4K}") == 1\n'
            f'    client = client.replace("{OLD2K}", "{h2k}").replace("{OLD4K}", "{h4k}")  # Triton-HC new-authority exact-depth hashes (A266/A267 pair)\n')
        (T / dst).write_text(s2); print(dst, 'written')

if __name__ == '__main__':
    main()
