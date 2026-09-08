# A331: both MTP1 records replay, but the gap between them does not separate from noise

A331 replayed A272, the Triton-HC lossless-MTP1 record, on overlay `62219122` with nothing
changed but attempt and port. (A330 was the first attempt and died in a card-0 engine reset
during weight load; the retry ran clean, and dmesg still shows only those two resets.)

## Both records reproduce

| lineage | published | replayed 2026-09-08 |
| --- | --- | --- |
| Triton-HC `62219122` | 37.045844 (A272) | **37.426051** (A331), +1.03% |
| fused-QSA `6d872457` | 37.825654 (A306) | 37.622275 (A328), 37.946213 (A329) |

Each published value falls inside the range its own replays span. Nothing here says either
record was wrong.

## But the improvement between them is not resolved by this evidence

| | value |
| --- | --- |
| gap as published (A306 − A272) | **+0.780 tok/s** |
| gap as replayed (mean of A328/A329 − A331) | **+0.358 tok/s** |
| measured MTP1 suite spread (three runs, one packet) | 0.324 peak-to-peak |
| warm rows 2–11, mean: A331 / A328 / A329 | 37.433 / 37.478 / 37.520 |

The replayed gap, +0.358, is about the size of the spread a *single* packet shows across
runs. On warm rows alone — excluding the cold rows 0 and 1 where JIT compilation lands — the
two lineages sit within 0.05–0.09 tok/s of each other.

**What this does and does not license.** It does not overturn the fused-QSA record: that
number was measured, gated and submitted, and it replays. It does say the published **+0.78
improvement over Triton-HC rests on one suite per side**, and that this lineage's
suite-to-suite spread is large enough that one suite per side cannot separate a 0.78 margin
with confidence. The measurement I have is consistent with a real but smaller improvement,
and also with much of that margin being run-to-run variation.

The right resolution is repeats: three suites on each overlay, compared as distributions
rather than single medians. That is roughly three hours of GPU time and is worth doing before
the +0.78 figure is repeated as a kernel-restoration result. I have not silently corrected
anything — the published records stand as measured, and this note is the caveat attached to
the comparison between them.

## Why this only surfaced now

Because nothing had ever replayed a Flash-Next record. Each was measured once, gated, and
published, and the next lineage was compared against the previous lineage's single number.
The spread that makes such a comparison fragile was itself unmeasured until A328/A329 tonight.
The MTP0 promotion earlier is unaffected: it cleared its control by 0.70 on four independent
runs against a 0.125 control spread, an order of magnitude better separated than this.

## Evidence

- `data/20260908-tp4-mtp1-a331-hctriton-record-replay-realistic-suite-v1-result.json`
- `data/20260908-tp4-mtp1-a32{8,9}-record-replay*-realistic-suite-v1-result.json`
- `data/20260907-tp4-mtp1-a306-qsafused-realistic-suite-v1-result.json`
- Packets: `tools/rewrite-q38-a272-to-a33{0,1}-mtp1-hctriton-suite-replay*.py` (pure replays).
