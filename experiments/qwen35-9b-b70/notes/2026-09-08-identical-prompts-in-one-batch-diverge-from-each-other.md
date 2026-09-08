# Identical prompts in the same batch diverge from each other

## The powered answer first: neither mechanism does anything

Filling the batch with the twelve prompts that carry the divergences worked as intended - the control
yielded 23 events against 9 for the whole suite, a 2.6x concentration. With that power the answer is
flat:

| arm | intervention | divergent / 1280 | tok/s |
| --- | --- | ---: | ---: |
| `f0` | none | 23 (`1.80%`) | `2093.6` |
| `f1` | row-wise all-reduce **and** serialised norm | 24 (`1.88%`) | `728.9` |

Two-sided binomial `p = 1.00`. The earlier monotone-looking 9, 7, 6, 3 across the under-powered arms
was noise, exactly as it was flagged to be at the time; at 2.6x the events the trend is simply gone.

So: **neither the cross-card all-reduce nor the norm's variance reduction, alone or together, has any
effect on the two-card divergence.** Both are demonstrably shape-dependent in isolation. Neither is
what flips these tokens. That closes the hypothesis the last several experiments were built on.

## Why, and it was free to find out

The targeted suite puts about five byte-identical copies of each prompt into every 64-slot batch.
That makes a diagnostic available that the diverse suite never could: **do copies of the same prompt,
issued together, agree with each other?**

They do not. In both arms, 23 of 240 prompt-groups per campaign contained copies that produced
different token arrays - six identical prompts in one batch returning two distinct completions.

Every copy in a group sees the same batch, the same row count, the same weights, the same greedy
decoding, and byte-identical input. Batch *size* cannot explain a difference between them, which is
why making the arithmetic invariant to batch size changed nothing. The lab has been chasing "the
result depends on how many rows share the step". What this shows is closer to **the result depends on
which row a request occupies**.

## The honest limit of that claim

Requests are issued concurrently but the scheduler is free to place them in different decode steps.
Two copies that drift apart by a step would see different step compositions, which would be shape
dependence again rather than position dependence. This measurement cannot separate those, because
the ladder records per-request outputs, not per-step batch membership.

What it does establish, without qualification, is the phenomenon in its sharpest form: **the same
input, submitted concurrently with itself, does not reliably produce the same output.** That is a
stronger and simpler statement than anything the concurrency ladders were reporting, and it is the
one worth designing the next experiment around.

## What to do next

1. Separate position from step composition. Log which requests share each decode step - or run the
   same prompt at a fixed pair of slots repeatedly - and see whether disagreement tracks slot index
   or step membership.
2. If it tracks slot index, the suspects change entirely: KV-cache block placement, attention tiling
   over the batch dimension, and the GDN state layout are position-dependent in a way the GEMM and
   the collective are not.
3. Stop testing shape-invariance interventions against this metric until that is settled. Two have
   now been ruled out at adequate power, and the reason they failed is visible in this data.

Evidence: `data/2026-09-08-fragile-site-identity.json`; targeted suite
`data/2026-09-08-fragile-tie-site-suite-v1.json`.
