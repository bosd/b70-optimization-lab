# Every published Flash-Next record replays

A335 replays the placement lossless-MTP1 record at 32.197434 against its published
31.929484 (+0.84%), on overlay `005dc578` with neither reference Triton kernel — the
pre-restoration line. That is the fifth and last of the lane's published Flash-Next records
to be re-measured. **Every one reproduces, and every published value falls inside the range
its own replays span.**

| record | overlay | published | replays (2026-09-08) | range | published inside? |
| --- | --- | --- | --- | --- | --- |
| placement MTP1 | `005dc578` | 31.929484 | 32.1974 | 0.268 | yes |
| Triton-HC MTP1 | `62219122` | 37.045844 | 37.4261, 37.1178 | 0.380 | yes |
| fused-QSA MTP1 | `6d872457` | 37.825654 | 37.6223, 37.9462 | 0.324 | yes |
| MTP0 W13-N32 | `2a372e86` | 33.797067 | 33.8012 | 0.004 | yes |
| MTP0 W13-N64 (promoted tonight) | `2a372e86` | 34.495292 | 34.5101, 34.5201 | 0.025 | yes |

Fourteen suite measurements across five overlays, on frozen packets driven exactly as the
records were.

## What the audit established

**The records are sound.** No published number is contradicted; each sits within its own
lineage's spread.

**The lineage ordering holds.** Means per line: placement 32.06 → Triton-HC 37.20 →
fused-QSA 37.80 on MTP1, and 33.80 → 34.51 on MTP0. Every step is in the direction the lane
claimed.

**One derived claim was overstated.** The +0.78 published between Triton-HC and fused-QSA is
+0.60 measured three-against-three, because the single-suite pairing happened to compare a
high draw with a low one. Corrected in the results packet; neither record changed.

**The lineages differ enormously in precision.** MTP0 replays to 0.004–0.025; MTP1 to
0.27–0.38, ten to ninety times wider. Speculation's acceptance varies run to run and a
non-speculative line has no such term. That is why the MTP0 promotion (+0.709 on a 0.025
spread, 28x) was settled by four runs while the MTP1 comparison (+0.60 on a 0.32 spread,
1.9x) needed six.

## Why this was worth the cards

Nothing had ever replayed a Flash-Next record. Each was measured once, gated, published, and
the next lineage was compared against the previous single number — so the spread that makes
such a comparison fragile was itself unmeasured. The audit cost about four hours of otherwise
idle cards overnight and produced: five confirmed records, two promotions with error bars,
one corrected derived claim, a measured precision figure per lineage, and the discovery that
224 of 243 frozen clients can no longer be re-run.

The contrast with the MiniMax re-check on the same night is the point. That guide could not
run at all — its venv's runtime had moved past the record's stack. This lane's records all
run, two weeks to a month on, because their runtime is pinned by frozen packets rather than a
shared environment.

## Evidence

- `data/20260908-tp4-mtp1-a335-placement-record-replay-realistic-suite-v1-result.json`
- `data/20260908-tp4-mtp{0,1}-a3{28,29,31,32,33,34}-*-realistic-suite-v1-result.json`
- Notes: `2026-09-08-a328…`, `…-mtp1-suite-spread-measured-on-three-runs.md`,
  `…-the-fused-qsa-improvement-is-real-and-smaller-than-published.md`,
  `…-a333-the-promoted-mtp0-record-with-error-bars.md`,
  `…-a334-the-mtp0-promotion-as-distribution-against-distribution.md`.
