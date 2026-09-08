# A322: the fresh-server repeat confirms removing the W13 delta

**Result.** A322 reran A321's configuration from a cold server on a reset host, same map,
same head, same frozen client.

| leg | A304 (N=32, certified) | A321 (N=64) | A322 (N=64) | A322 − A304 |
| --- | --- | --- | --- | --- |
| exact-2K r1 | 33.322 | 34.127 | 34.193 | +0.871 |
| exact-2K r2 | 33.447 | 34.170 | 34.165 | +0.719 |
| exact-4K r1 | 33.471 | 34.096 | 34.105 | +0.634 |
| exact-4K r2 | 33.410 | 34.034 | 34.098 | +0.688 |

A321 mean **+0.695**, A322 mean **+0.728** tok/s. The two independent runs agree to within
**0.066 tok/s on every row** — tighter than A304's own 0.125 spread between its two exact-2K
rows. Hashes unmoved on all four rows; gates
`PASS recovery quality short-repeat exact-2K-repeat exact-4K-repeat`.

**What is now established.** Neutralising the certified W13 phase delta is a reproducible,
lossless gain of about +0.7 tok/s (+2.1%) on the MTP0 lineage's exact-depth rows, from a
one-line map change with no source change and the certified head unmodified.

**What is still required before the record moves.** The published MTP0 figure, 33.797067
tok/s, is the median of twelve `tok_s_1_100_intervals_after_ttft` rows in A301's realistic
suite — not an exact-depth row. A323 runs A301's own suite client on this configuration so
the medians are directly comparable. Until it reports, the honest claim is "+0.7 tok/s on
the exact-depth rows, confirmed twice", not a new record.

## Evidence

- `data/20260908-tp4-mtp0-a322-w13n64-repeat-exact-depth-{2k,4k}-r{1,2}.json` — the four rows.
- `data/20260908-tp4-mtp0-a322-w13n64-repeat-moe-m1-w13-n64-selection-receipt.json` — the
  in-run receipt, `status pass`, key 1, W13 N=64, W2 N=64.
- `data/20260908-tp4-mtp0-a322-w13n64-repeat-client-gates-passed.txt`, `…-quality-current.json`,
  `…-identity.txt`.
- Packet: `tools/rewrite-q38-a304-to-a322-mtp0-w13-blockn64-repeat.py`, head `2a372e86`.
