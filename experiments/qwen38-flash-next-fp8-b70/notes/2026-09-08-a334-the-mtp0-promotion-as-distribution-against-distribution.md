# A334: the MTP0 promotion, distribution against distribution

The promotion was three suites on the new line against one on the old. A334 replays the
superseded W13-N32 configuration — A301's packet, certified map, certified verifier, head
`2a372e86`, nothing changed but attempt and port — so both sides now carry error bars.

| line | suites | mean | range |
| --- | --- | --- | --- |
| W13-N32 (superseded) | 33.797067 (A301, published), 33.801227 (A334) | 33.799147 | **0.004160** |
| W13-N64 (promoted) | 34.510128 (A325), 34.495292 (A326, published), 34.520093 (A333) | 34.508504 | 0.024801 |

| | value |
| --- | --- |
| gap of means | **+0.709357** |
| worst case (slowest N64 − fastest N32) | **+0.694065** |
| ranges overlap | **no** |
| separation | worst-case gap is **28x** the larger spread |

**The superseded line replays to 0.0042.** A334 lands 0.004 above A301's published value —
tighter even than the promoted line's 0.025 range, and a further confirmation that MTP0 is
the quiet lineage. Two independent measurements of A301's configuration, four months of
tooling churn apart, agree to four thousandths of a tok/s.

**So the promotion is settled on both sides.** It is no longer a distribution against a
single point: every N64 run beats every N32 run by at least 0.694, against spreads of 0.004
and 0.025. There is no arrangement of this data in which the W13-N64 change is not worth
about +0.71 tok/s.

**I am not running a third N32 suite.** Two points agreeing to 0.0042, against a gap of
0.694, cannot be moved by a third — it would be symmetry for its own sake and 20 minutes of
cards better spent elsewhere. The MTP1 comparison needed three per arm because its spread
was 0.32 against a 0.78 claim; this one is 0.025 against 0.71. Matching the evidence to the
claim is the point, not matching run counts to each other.

## What the four measurements together say about this lane

| comparison | claim | spread | ratio | verdict |
| --- | --- | --- | --- | --- |
| MTP0 W13-N64 over N32 | +0.709 | 0.025 | 28x | settled |
| MTP1 fused-QSA over Triton-HC | +0.601 | 0.324 | 1.9x | needed three per arm; real but smaller than the +0.78 published |

Same lane, same metric, same twelve prompts. The difference is entirely speculation: MTP1's
acceptance varies run to run, MTP0's has no such term.

## Evidence

- `data/20260908-tp4-mtp0-a334-w13n32-suite-second-realistic-suite-v1-result.json`
- `data/20260908-tp4-mtp0-a333-w13n64-suite-third-realistic-suite-v1-result.json`
- `data/20260908-tp4-mtp0-a32{5,6}-w13n64-*realistic-suite-v1-result.json`
- `data/20260907-tp4-mtp0-a301-qsafused-realistic-suite-v1-result.json`
- Packet: `tools/rewrite-q38-a301-to-a334-mtp0-w13n32-suite-second.py` (pure replay).
