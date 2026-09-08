# A338: the guide's own gate passes, and my cross-lineage number moves again

A338 replayed the fused-QSA MTP1 record through **the guide's own published path** —
`run-record-gate.sh`, which verified the identity chain and all three git bundles, derived
the packet, passed static validation, launched, ran the client, and judged the result.

**The guide's verdict: `PASS: bit-identical outputs and all gates hold`**, with the replay
median at 37.074497 against the record's 37.825654. The record is validated on the guide's own
criterion, by the path a reader would actually follow. That is the headline and it is good.

## But the median is the lowest of four, and it breaks my earlier claim

| fused-QSA `6d872457` | | Triton-HC `62219122` | |
| --- | --- | --- | --- |
| A306 (published) | 37.825654 | A272 (published) | 37.045844 |
| A328 | 37.622275 | A331 | 37.426051 |
| A329 | 37.946213 | A332 | 37.117799 |
| **A338 (guide gate)** | **37.074497** | | |
| mean 37.6172, sd 0.334, range 0.872 | | mean 37.1966, sd 0.165, range 0.380 | |

| comparison | gap of means | ranges overlap? |
| --- | --- | --- |
| 3 v 3, as I published this morning | +0.6015 | **no** |
| 4 v 3, with A338 | **+0.4206** | **yes** — 37.0745 against 37.4261 |

I wrote, in the results packet, that "the ranges do not overlap — the slowest fused-QSA run
beats the fastest Triton-HC run by 0.1962". **With a fourth sample that is false.** The
non-overlap was luck of the draw across three runs, not a property of the lineages.

## It is not a client-path artefact

A338 ran through the guide's `wait-and-run-client.sh` while A306/A328/A329 used
`q38-suite-driver.sh`. I checked before concluding: the two invoke
`bench-openai-realistic-suite.py` with identical arguments — same suite file, `--max-tokens
512`, `--metric-tokens 100`, `--seed 20260609`, same `--request-extra-json`. They differ only
in a `timeout` wrapper and how they print. A338 is a genuine draw from the same distribution.

## What I should say instead of a number

The fused-QSA sd is **0.334** over four suites — twice the 0.134 that three suggested, and
comparable to the whole effect being measured. Three of four fused-QSA runs still exceed every
Triton-HC run, and the means still differ by +0.42 in the expected direction, so the
improvement is probably real. But **this lineage cannot support a point estimate of the gap at
the precision I have been quoting it**, and I have now quoted three different values in one
session: +0.78 published, +0.60 after 3v3, +0.42 after 4v3.

The honest statement is: *restoring the fused QSA pre-indexer is worth something on the order
of half a tok/s on MTP1, and the measurement noise on that lineage is of the same order.*
Anything sharper needs a paired design — same host, alternating arms, many more runs — not
another suite bolted onto one side.

The MTP0 promotion is untouched by this. Its margin is +0.68 worst case against an sd of
0.016: a fortyfold separation, which is why four samples moved it not at all.

## Evidence

- `data/20260908-tp4-mtp1-a338-guide-gate-replay-realistic-suite-v1-result.json`
- Gate transcript: identity chain `6d872457` over `62219122` over `005dc578` over `1b2a17c1`
  over `76cfe1cd`, stage `2f829747`, oneCCL `4ceafd1`, model `bcd9f01d`; packet a338 derived
  and statically validated; `PASS: bit-identical outputs and all gates hold`.
- Supersedes the gap figure in
  `notes/2026-09-08-the-fused-qsa-improvement-is-real-and-smaller-than-published.md` and the
  paragraph it added to `results/qwen38-flash-next-fp8-b70/README.md`.
