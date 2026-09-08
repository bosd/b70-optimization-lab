# Three suites per overlay: the fused-QSA improvement is real, and smaller than published

A331 raised a fair doubt — the +0.780 tok/s published between the Triton-HC and fused-QSA
lineages came from one suite per side, and one suite per side cannot separate that from this
lineage's run-to-run spread. A332 supplies the third Triton-HC suite, so the comparison is
now three against three, read as distributions.

| overlay | suites (class-balanced median) | mean | median | range | sd |
| --- | --- | --- | --- | --- | --- |
| Triton-HC `62219122` | 37.045844 (A272, published), 37.426051 (A331), 37.117799 (A332) | **37.1966** | 37.1178 | 0.3802 | 0.165 |
| fused-QSA `6d872457` | 37.825654 (A306, published), 37.622275 (A328), 37.946213 (A329) | **37.7980** | 37.8257 | 0.3239 | 0.134 |

**The ranges do not overlap.** The slowest fused-QSA run (37.6223) is above the fastest
Triton-HC run (37.4261), a worst-case margin of **+0.1962**. Three runs against three, every
pairing in the same direction.

**So the improvement is real.** The doubt A331 raised is answered, and answered in favour of
the published claim's direction.

**And it is smaller than published.**

| comparison | gap |
| --- | --- |
| published, single suite each | +0.7798 |
| means of three | **+0.6015** |
| medians of three | +0.7079 |
| worst case (slowest QSA − fastest HC) | +0.1962 |

The honest figure for the fused-QSA pre-indexer restoration over the Triton-HC line is
**about +0.60 tok/s (+1.6%)**, not +0.78. The single-suite comparison happened to pair a
high fused-QSA draw with a low Triton-HC draw; both published values sit inside their own
lineage's replay range, so neither was wrong, but their difference was inflated by about
0.18 by the luck of which runs were compared.

**Nothing is retracted.** Both records were measured, gated, submitted and replay. The
LocalMaxxing rows stand. What changes is the *derived* claim about the size of the step
between them, which is a comparison this lane makes in prose rather than a submitted number.

**The general rule, now demonstrated rather than asserted.** On MTP1, a single suite per arm
supports no claim below roughly ±0.3 tok/s. This comparison needed three per arm to become
sound, and it cost about an hour of otherwise idle cards. The MTP0 line does not need this —
its suites agree to 0.015 — so the requirement is specific to speculative decoding, where
acceptance varies run to run.

## Evidence

- `data/20260908-tp4-mtp1-a332-hctriton-suite-third-realistic-suite-v1-result.json` (A332)
- `data/20260908-tp4-mtp1-a331-hctriton-record-replay-realistic-suite-v1-result.json` (A331)
- `data/20260908-tp4-mtp1-a32{8,9}-record-replay*-realistic-suite-v1-result.json` (A328/A329)
- `data/20260907-tp4-mtp1-a306-qsafused-realistic-suite-v1-result.json` (A306, published)
- The A272 published median is quoted from `results/qwen38-flash-next-fp8-b70/README.md`.
- Supersedes the open question in
  `notes/2026-09-08-a331-both-mtp1-records-replay-but-the-gap-between-them-does-not-separate.md`.
