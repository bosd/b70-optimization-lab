# A constant-composition batch is deterministic; the ladder's is not

## What was tried

The per-layer probe showed the body bitwise deterministic for rows at the same generation position,
but that run did not reproduce the divergence - all 64 outputs were byte-identical. Two differences
from the ladder were the suspects: it ran eager where the ladder uses full decode-only graph capture,
and it ran unspeculated.

Graph capture was the stronger suspect, since a replayed graph is shape-specialised. Re-run with
`FULL_DECODE_ONLY` capture at sizes 1 to 64, matching the ladder: **still 64 identical outputs**.
Graph capture does not reproduce it either.

(The layer hook cannot be used in that mode: it converts tensors to numpy, which graph capture
rejects with "Unsupported ndarray method call", and a replayed graph bypasses Python hooks anyway.
The output comparison is the measurement there.)

## What is left, and it is not a detail

The offline probe submits 64 identical prompts at once, all the same length, all generating to the
same cap. They stay in lockstep: every step has the same 64 rows, at the same position, in the same
composition, from first token to last.

The ladder does not. Its requests drift - measured directly from the ladder timings at about three
decode steps of spread - so the number of rows in a step and which requests share it change as
generation proceeds. A request's token N is computed in a differently-composed step than it would be
in the single-request oracle.

That is the difference that survives, and it reframes the target:

- **A batch of constant composition is deterministic**, at 64 rows, on two cards, eager or graph.
- The divergence needs the composition to *vary*, which is what a real server does.

## Why the interventions all failed

It also explains four negatives in one stroke. The norm is row-count dependent from 16 rows and the
vocabulary projection from 33; making either one invariant leaves the other, and leaves whatever else
in the body shares the property. If the mechanism is "a request's step composition differs from the
oracle's", then every row-count-dependent op contributes, and fixing them one at a time cannot move
the number - which is exactly what four powered arms found.

## What to do next

Reproduce the divergence offline by inducing drift, rather than reaching for another op. Submitting
the same 64 prompts with staggered arrival, or with unequal generation caps so requests finish at
different times, should make the composition vary the way the server's does. If that reproduces it in
a controlled process, every question after it gets cheaper - including which op, because the layer
hook already works in eager mode and would then have a divergence to bisect.

Evidence: `data/2026-09-08-layer-hash-decode-position-grouped-tp2.tsv`; probe
`probes/layer-hash-offline-prefill.py`.
