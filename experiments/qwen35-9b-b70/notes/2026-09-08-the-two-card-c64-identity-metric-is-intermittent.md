# The two-card c64 identity metric is intermittent, and two passes cannot resolve an intervention

## What happened

The serialised-norm experiment's control arm - the diagnostic overlay with serialisation switched
**off**, which is functionally R276 - scored `64/64` at 64 concurrent users in both passes. The
published result for that same configuration is `63/64` in both passes, and the row-wise all-reduce
overlay's control also scored `63/64` in both passes.

So the control is not stable:

| campaign | intervention | pass 1 | pass 2 |
| --- | --- | --- | --- |
| `w3` (stock R276) | none | 63/64 | 63/64 |
| `r0` (row-wise overlay, off) | none | 63/64 | 63/64 |
| `s0` (serial-norm overlay, off) | none | **64/64** | **64/64** |
| `r1` (row-wise overlay, on) | row-wise all-reduce | 64/64 | 63/64 |

Six control passes: four at `63/64`, two at `64/64`. Throughput is tight across all of them
(`2083.7`-`2093.6 tok/s`) and every strict gate is 12/12 everywhere, so this is not a broken run or a
different configuration. The single lost request at 64 users simply does not appear every time.

## What it invalidates

The row-wise all-reduce write-up leaned on the control having scored `63/64` four times across two
images, and read `r1`'s `64/64` then `63/64` as failing to beat a stable baseline. The baseline was
not stable. That sample of the control distribution was unrepresentative, and `r1`'s result sits
inside it.

The conclusion in that note - that the row-wise all-reduce is not a demonstrated fix - survives, and
in fact hardens: it was never demonstrated, because the comparison never had the resolution to
demonstrate anything. What does not survive is the reasoning, which treated two passes of a control
as a baseline. It was not one.

This applies equally to the arm running now. The serialised-norm measurement will produce a cost
figure that is meaningful, and an identity figure that is not.

## Why the metric behaves this way

It fits the norm finding rather than contradicting it. The norm gives a small fraction of rows a
last-bit perturbation once the batch reaches 16, and a perturbation only changes a token when it
lands on a near-tie. Whether any near-tie in a 64-request batch coincides with a perturbed row is a
matter of which rows land where, which varies with scheduling between campaigns. A metric built on
"did at least one of 64 requests diverge" is a Bernoulli draw over that coincidence, and at a rate
near one miss per 64 requests, two draws carry almost no information.

## What to measure instead

Counting **total divergent requests over many repeats** converges far faster than a per-rung pass or
fail, because it uses every request rather than collapsing 64 of them into one bit. Two changes make
these comparisons decidable:

1. Report the divergent-request rate with its sample size, not `n/64` from a single pass.
2. Size the arms from the observed control rate. At roughly one miss per 64-128 requests, separating
   "usually one miss" from "never a miss" needs on the order of tens of passes per arm, not two.

Until that is done, no intervention should be described as fixing or failing to fix the two-card
gap. The one-card ladders are unaffected: they are exact at every rung in both passes with no misses
at all, and a claim of zero misses over many requests does not have this problem - it is the
near-zero-rate comparisons that two passes cannot separate.

Evidence: campaign roots `qwen35-9b-w4a16-tp2-mtp3-graph1-dhint4-20260907-w3`,
`qwen35-9b-w4a16-tp2-rowwise-r0`, `qwen35-9b-w4a16-tp2-rowwise-r1`,
`qwen35-9b-w4a16-tp2-serialnorm-s0`.
