# A333: the promoted MTP0 record, now with error bars

The record submitted tonight rested on two suites. The MTP1 work then showed that a tight
pair can still leave a comparison underdetermined, so it would have been inconsistent to
demand three suites of the older records and leave the newest on two. A333 is the third.

## The promoted line

| suite | class-balanced median |
| --- | --- |
| A325 | 34.510128 |
| A326 (**published headline**) | 34.495292 |
| A333 | 34.520093 |

Mean **34.508504**, median 34.510128, range **0.024801**, sd 0.0102.

The published headline is the **lowest of the three**. Choosing the lower of the pair at
promotion time turned out to understate the line by 0.013 against the mean, which is the
direction an error should go.

## MTP0 really is the quieter lineage

| lineage | peak-to-peak over three suites |
| --- | --- |
| MTP0 W13-N64 | **0.0248** |
| MTP1 fused-QSA | 0.3239 (13.1x wider) |
| MTP1 Triton-HC | 0.3802 (15.3x wider) |

So the claim from A329 holds, with one correction: I said "roughly twenty times tighter"
from a two-suite pair; measured over three suites each it is **13–15x**, not 20x. Same
conclusion, smaller number, and the mechanism is unchanged — speculation acceptance varies
run to run and a non-speculative line has no such term.

## The promotion is very well separated

Against the superseded 33.797067: **+0.7114 on means, +0.6982 worst case** — and that worst
case is **28x** the MTP0 spread. There is no reading of this data in which the promotion was
noise, which is what the four independent exact-depth runs already suggested and this now
confirms on the suite metric itself.

Contrast with the cross-lineage MTP1 comparison, where the published gap was +0.78 against a
spread of 0.32 — 2.4x — and needed three suites per arm to establish, ending at +0.60. Same
lane, same metric, two claims an order of magnitude apart in how well they were supported.

## Nothing changes on the published surface

The submitted number stays 34.495292: it is a real measurement, it is the conservative one of
three, and re-submitting a mean would be churn for +0.013. This note is the error bar behind
it, not a revision of it.

## Evidence

- `data/20260908-tp4-mtp0-a333-w13n64-suite-third-realistic-suite-v1-result.json`
- `data/20260908-tp4-mtp0-a32{5,6}-w13n64-*realistic-suite-v1-result.json`
- Packet: `tools/rewrite-q38-a301-to-a333-mtp0-w13-blockn64-suite-third.py`, head `2a372e86`,
  map `moe-m1-w13-n64` — identical to A325/A326 but for attempt and port.
