# Qwen3.5-4B FP8-dynamic is not repeat-exact on this stack (2026-09-07)

A negative result, recorded so nobody repeats it: the 4B FP8 route cannot pass the lab's base identity gate, so no
lossless claim and no package come from it. The same stack passes that gate on the 9B every time.

## What ran

`RedHatAI/Qwen3.5-4B-FP8-dynamic` at revision `397b7ba4…` (8.05 GB, ships an MTP head), one B70, R276 image, the strict
launchers, full decode-only XPU graph capture, no speculation, one slot, `max-model-len 1024`, cache zero, canaries on
every server. Three independent campaigns (`q1`, `q2`, `q3`), two fresh servers each with separate empty compile caches:
six samples of exactly the same configuration. Decode was steady across all six, 82.18 to 82.42 tok/s class-balanced
median, so nothing about the runs was unhealthy.

## Result

The gate is G1: two fresh servers of the same configuration must produce byte-identical complete token arrays on all
twelve prompts. The three pairs scored **11/12, 9/12 and 11/12**. Across all fifteen pairwise comparisons of the six
samples the count ranges from 9/12 to 12/12 (mean 10.3): one pair happened to agree completely, which is why a single
pair is not evidence of determinism.

Exactly **three of the twelve prompts are tie-prone**, and each has exactly **two** variants. The other nine prompts are
identical in all six samples.

| prompt | first divergent token | servers on variant A | servers on variant B |
| --- | ---: | --- | --- |
| `performance-hypotheses` | 8 | q1a q1b q2b q3a | q2a q3b |
| `code-review` | 284 | q1a q2a q3a q3b | q1b q2b |
| `benchmark-analysis` | 421 | q1a q1b q2b | q2a q3a q3b |

Both continuations are ordinary and correct. At `code-review` token 284 one variant writes "a dedicated **table in the
DB**" and the other "a dedicated **`failed_events` table**".

## Reading it

Never three variants, always two, and servers land on either side independently: that is a tie in the next-token scores
being resolved by per-process state, not drift, not a harness fault, and not a quality problem. Nine prompts never move,
so the run itself is reproducible; only the tied positions are free.

This is the same mechanism the lab sees at high concurrency on the FP8 lanes, where a handful of prompts flip once the
batch grows. The 9B W4A16 measurement on the same day showed that class of flip disappears on the row-invariant
W4A16 INT4 kernel, which does not change its reduction order with row count: there, every concurrency rung through 64
users is byte-exact in both passes. The 4B W4A16 route (`RedHatAI/Qwen3.5-4B-quantized.w4a16`, `7a613872…`) is the
direct test of whether that also fixes the fresh-server case on this model, and it is measured next.

Evidence: `data/2026-09-07-qwen35-4b-fp8-repeat-exactness.json`, campaign roots
`qwen35-4b-fp8-tp1-mtp3-graph1-dhint4-20260907-q{1,2,3}`.
