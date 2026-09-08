# A339: the balanced comparison, and the number I will stand behind

A338 left the MTP1 cross-lineage comparison at four fused-QSA suites against three Triton-HC,
which flatters whichever arm has fewer draws. A339 is the fourth Triton-HC suite. This is the
balanced version.

| overlay | suites (sorted) | mean | sd | range |
| --- | --- | --- | --- | --- |
| Triton-HC `62219122` | 37.0373, 37.0458, 37.1178, 37.4261 | 37.1567 | 0.159 | 0.389 |
| fused-QSA `6d872457` | 37.0745, 37.6223, 37.8257, 37.9462 | **37.6172** | 0.334 | 0.872 |

| | |
| --- | --- |
| gap of means | **+0.4604 tok/s** |
| standard error of that difference | ~0.185 |
| difference in standard errors | ~2.5 |
| ranges overlap | yes — 37.0745 against 37.4261 |
| fused-QSA runs above every Triton-HC run | 3 of 4 |

## What this supports

A real improvement of **about +0.46 tok/s (+1.2%)** from restoring the fused QSA pre-indexer,
at roughly 2.5 standard errors. That is meaningful evidence, not proof: three of four
fused-QSA runs beat every Triton-HC run, and the fourth does not.

## The history of this one number, which is the actual lesson

| stage | value | why it changed |
| --- | --- | --- |
| published | +0.7798 | one suite per side |
| after 3v3 | +0.6015 | both sides replayed three times |
| after 4v3 | +0.4206 | a fourth fused-QSA suite, lowest of its arm |
| **after 4v4** | **+0.4604** | balanced; the honest figure |

The estimate moved by 0.32 tok/s — most of the effect being measured — purely from adding
samples. Every intermediate value was reported as if it were the answer, including by me,
twice. The lineage's noise (fused-QSA sd 0.334) is comparable to the effect, and that is the
durable fact: **on MTP1 a difference of half a tok/s needs many runs per arm, and a single
suite per side cannot see it at all.**

## Against MTP0

The MTP0 promotion measured +0.71 with an sd of 0.016 — a fortyfold separation that did not
move as samples accumulated. Same lane, same metric, same twelve prompts. Speculation's
run-to-run acceptance is the entire difference, and it is why the two claims deserve very
different confidence.

## Evidence

- `data/20260908-tp4-mtp1-a339-hctriton-suite-fourth-realistic-suite-v1-result.json`
- The other seven suites are listed in
  `notes/2026-09-08-a338-the-mtp1-cross-lineage-gap-does-not-hold-a-point-estimate.md`.
- Supersedes the gap figures in that note and in
  `notes/2026-09-08-the-fused-qsa-improvement-is-real-and-smaller-than-published.md`.
