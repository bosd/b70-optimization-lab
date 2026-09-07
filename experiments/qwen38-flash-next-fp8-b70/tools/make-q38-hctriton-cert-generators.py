#!/usr/bin/env python3
"""Derive the HC-Triton new-authority certification generators (A266 MTP0 battery, A267 MTP0 suite,
A268 MTP1 battery, A269 MTP1 suite) from the split-K 4 v2 certification generators (A259-A262):
candidate heads 2aa369a6 / b0836afb, VLLM_XPU_HC_TRITON=1 in the derived source, identity literal
…_splitk4_hctriton, and the frozen client's exact-depth authority literals repinned to the new
2K/4K hashes established by the A263/A264 fresh-server pair (MTP1 hashes default to the MTP0 ones:
lossless MTP1 must reproduce them).

  make-q38-hctriton-cert-generators.py --hash2k <sha256> --hash4k <sha256> [--mtp1-hash2k …] [--mtp1-hash4k …]
"""
import argparse, re
from pathlib import Path
T = Path(__file__).resolve().parent
HASH = re.compile(r'[0-9a-f]{12,}')
OLD2K = 'afffd2110812762164862b6388f054bb56696ee57b07eadce411a702c40bc714'
OLD4K = 'c6193cc6c9a1553f56d7ce78faea9c8bfa628a67fcea229b1c99279a149f6639'
PLAN = [  # (src gen, dst gen, old attempt, new attempt, old port, new port, head swap, mtp1?)
    ('rewrite-q38-a78-to-a259-placement-splitk4v2-frozen-client.py', 'rewrite-q38-a78-to-a266-placement-splitk4v2-hctriton-frozen-client.py', 259, 266, '19925', '19932', ('82b9f9cf34f8a04a6338cb256667f13c9f841b31', '2aa369a6c069e64579c62905e0cfee8b456d8cc3'), False),
    ('rewrite-q38-a78-to-a260-placement-splitk4v2-realistic-suite.py', 'rewrite-q38-a78-to-a267-placement-splitk4v2-hctriton-realistic-suite.py', 260, 267, '19926', '19933', ('82b9f9cf34f8a04a6338cb256667f13c9f841b31', '2aa369a6c069e64579c62905e0cfee8b456d8cc3'), False),
    ('rewrite-q38-a120-to-a261-mtp1-placement-splitk4v2-frozen-client.py', 'rewrite-q38-a120-to-a268-mtp1-placement-splitk4v2-hctriton-frozen-client.py', 261, 268, '19927', '19934', ('893e1ccc7a1e681b861a1f28c6a6f59cade677dc', 'b0836afbc5eafbe9ab4728c89b43dd10c3efac7a'), True),
    ('rewrite-q38-a120-to-a262-mtp1-placement-splitk4v2-realistic-suite.py', 'rewrite-q38-a120-to-a269-mtp1-placement-splitk4v2-hctriton-realistic-suite.py', 262, 269, '19928', '19935', ('893e1ccc7a1e681b861a1f28c6a6f59cade677dc', 'b0836afbc5eafbe9ab4728c89b43dd10c3efac7a'), True),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hash2k', required=True); ap.add_argument('--hash4k', required=True)
    ap.add_argument('--mtp1-hash2k'); ap.add_argument('--mtp1-hash4k')
    a = ap.parse_args()
    for h in (a.hash2k, a.hash4k, a.mtp1_hash2k or a.hash2k, a.mtp1_hash4k or a.hash4k):
        assert re.fullmatch(r'[0-9a-f]{64}', h), h
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
            out.append(h); pos = m.end()
        out.append(sub(s[pos:])); s2 = ''.join(out)
        key = 'cold_expert_host_placement_splitk4v2'
        assert s2.count(key) == 1, (src, key); s2 = s2.replace(key, key + '_hctriton')
        key = '  print "export VLLM_XPU_MOE_SPLIT_K=4"\\n\')'
        assert s2.count(key) == 1, (src, key)
        s2 = s2.replace(key, '  print "export VLLM_XPU_MOE_SPLIT_K=4"\\n  print "export VLLM_XPU_HC_TRITON=1"\\n\')')
        key = '    client = client.replace(OLD_HEAD, NEW_HEAD)\n'
        assert s2.count(key) == 1, (src, key)
        s2 = s2.replace(key, key +
            f'    assert client.count("{OLD2K}") == 1 and client.count("{OLD4K}") == 1\n'
            f'    client = client.replace("{OLD2K}", "{h2k}").replace("{OLD4K}", "{h4k}")  # HC-Triton new-authority exact-depth hashes (A252/A253 pair)\n')
        (T / dst).write_text(s2); print(dst, 'written')

if __name__ == '__main__':
    main()
