#!/usr/bin/env python3
"""Derive the HC-Triton new-authority certification generators (A255 MTP0 battery, A256 MTP0 suite,
A257 MTP1 battery, A258 MTP1 suite) from the split-K 4 certification generators (A248-A251):
candidate heads 09279b6a / f57d40d7, VLLM_XPU_HC_TRITON=1 in the derived source, identity literal
…_splitk4_hctriton, and the frozen client's exact-depth authority literals repinned to the new
2K/4K hashes established by the A252/A253 fresh-server pair (MTP1 hashes default to the MTP0 ones:
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
    ('rewrite-q38-a78-to-a248-placement-splitk4-frozen-client.py', 'rewrite-q38-a78-to-a255-placement-splitk4-hctriton-frozen-client.py', 248, 255, '19893', '19921', ('6a79c56d8a980aaa3858e2b3f004761e90d18e45', '09279b6ae612f84b130ef27f04443101ad9d42a8'), False),
    ('rewrite-q38-a78-to-a249-placement-splitk4-realistic-suite.py', 'rewrite-q38-a78-to-a256-placement-splitk4-hctriton-realistic-suite.py', 249, 256, '19897', '19922', ('6a79c56d8a980aaa3858e2b3f004761e90d18e45', '09279b6ae612f84b130ef27f04443101ad9d42a8'), False),
    ('rewrite-q38-a120-to-a250-mtp1-placement-splitk4-frozen-client.py', 'rewrite-q38-a120-to-a257-mtp1-placement-splitk4-hctriton-frozen-client.py', 250, 257, '19895', '19923', ('e9e65888981a880b8298143f571f276c8c52e4a9', 'f57d40d759861ed0943316756efd9a7f69aaa7a4'), True),
    ('rewrite-q38-a120-to-a251-mtp1-placement-splitk4-realistic-suite.py', 'rewrite-q38-a120-to-a258-mtp1-placement-splitk4-hctriton-realistic-suite.py', 251, 258, '19896', '19924', ('e9e65888981a880b8298143f571f276c8c52e4a9', 'f57d40d759861ed0943316756efd9a7f69aaa7a4'), True),
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
        key = 'cold_expert_host_placement_splitk4'
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
