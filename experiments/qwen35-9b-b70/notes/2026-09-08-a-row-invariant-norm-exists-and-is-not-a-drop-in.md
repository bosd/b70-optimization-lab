# A row-invariant norm exists on this hardware, and it is not a drop-in

## Why this was the next question

The row-wise all-reduce experiment ruled out the cross-card collective as the sole cause of the
two-card identity loss, and the probe that followed found why: the RMSNorm Qwen3.5 runs is itself
row-count dependent, giving about 2-3% of rows a last-bit difference once the batch reaches 16.

Before that can be fixed end to end, something has to be established first: does a row-invariant
implementation of the same maths exist on this hardware at all? If the answer were no - if every
way of computing it on this stack varied with batch shape - the whole line of work would be closed
and the two-card gap would be a hardware property rather than a bug.

## Result: yes, and the obvious candidate is the wrong one

Four implementations of the same function, five seeds each, float16 at hidden 4096:

| implementation | differing rows at 128 | rate | us/forward |
| --- | ---: | ---: | ---: |
| `native` (what the server runs, `ir.ops.rms_norm`) | 16/640 | `2.50%` | `50.1` |
| `torch_fp16` (`x * rsqrt(mean(x^2)+eps) * w`, all float16) | **0/640** | `0.00%` | `28.9` |
| `torch_fp32` (same, reduction accumulated in float32) | 49/640 | `7.66%` | `41.4` |
| `rowwise` (each row alone, invariant by construction) | **0/640** | `0.00%` | `5446.5` |

Two things worth taking from that table beyond the headline.

**Float32 accumulation makes it worse.** That is the first thing most people would reach for, and on
this stack it triples the dependence rather than removing it. More precision in the accumulator does
not buy shape independence; whatever varies is the reduction's structure, not its width, and the
wider accumulator appears to change the structure unfavourably. Anyone attacking this should not
spend a day on float32.

**The naive fix costs about 108x.** Normalising each row alone is invariant by construction and runs
at `5446 us` against `29-50 us`. That is the same shape as the row-wise all-reduce result - correct
and unusable - and it is why an actually-invariant kernel is worth building rather than just looping.

## The caveat that matters

`torch_fp16` is **not** a drop-in replacement. It does not reproduce the current op's values: the
two differ by up to 3 ULP, and most rows differ even at a single row, so it is a different rounding
of the same function rather than a patch.

Adopting it would change model outputs, invalidate every published output hash for these lanes, and
require re-running the full identity chain from scratch. The new outputs would be equally valid - it
is the same function - but they would not be today's outputs, and every G1/G2/G3 result and every
recorded SHA would have to be regenerated against it.

So this is an existence proof, not a change to make. What it establishes is that the property is
achievable on this hardware and is not obviously expensive, which is what was actually in doubt.

Do not read the timing column as a 42% win, either. At 128x4096 float16 the tensor is about 1 MB,
a few microseconds of bandwidth against 29-50 us measured, so both figures are dominated by launch
and dispatch overhead. The honest reading is "not obviously more expensive", not "faster".

## What would settle it

1. Find out what the native op's reduction does differently. It is `ir.ops.rms_norm`; if its
   shape-dependence is a tiling choice, pinning that choice is the cheap fix and preserves values.
   That is the version worth having, because it needs no re-qualification.
2. If it cannot be pinned, decide whether a re-qualified lane is worth it. The prize is the two-card
   identity gap and possibly the 96-user miss on one card; the price is regenerating every hash.
3. Either way, re-run the two-card ladder with an invariant norm *and* the row-wise all-reduce
   together. The r0/r1 arms showed the collective alone is not enough; the pair has never been tried,
   and this note is what makes trying it possible.

Evidence: `data/2026-09-08-rmsnorm-variant-row-invariance.json`; probes
`probes/rmsnorm-variant-row-invariance.py` and `probes/rmsnorm-native-vs-torch-agreement.py`.
