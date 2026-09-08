# The norm is row-count dependent too

## Why this was asked

The lab's account of output identity has been about the matmul: a kernel that sums a row differently
depending on how many rows share the batch can flip a token whose top two candidates are tied, and
the INT4 W4A16 GEMM is row-count invariant by construction, which is why that route is byte-exact
where FP8 is not. Four independent measurements support it, most recently the depth sweep, where
every draft depth from 3 to 6 stayed lossless on W4A16 while FP8 held only at 3.

But the two-card residue does not fit. Forcing every cross-card reduction onto the single-row path
(campaigns r0/r1) did not reliably restore identity, so something else on that path is also
shape-dependent. The Flash-Next lane had already met this: it needed two row-wise switches, and the
second existed because a grouped RMSNorm's mean was reduced in a shape-dependent order.

So: is the norm Qwen3.5 actually runs here row-count invariant? Nobody had checked.

## Method

No server, no second card. The op is built inside a vLLM config context (it is a `CustomOp` and
picks its implementation at construction) and fed the same rows alone and batched, comparing
outputs bitwise in float16, the serving dtype. The forward it dispatches is `forward_native`, which
matches what the server selects - the startup log reports
`IrOpPriorityConfig(rms_norm=['native'])` - and which lowers to `ir.ops.rms_norm`.

Probe: `probes/rmsnorm-row-invariance-probe.py`.

## Result: it is not invariant

Ten seeds per row count, hidden 4096:

| rows in batch | rows differing from the same row alone | rate |
| ---: | ---: | ---: |
| 1 | 0/10 | 0.00% |
| 2 | 0/20 | 0.00% |
| 4 | 0/40 | 0.00% |
| 8 | 0/80 | 0.00% |
| 16 | 3/160 | 1.88% |
| 32 | 9/320 | 2.81% |
| 64 | 19/640 | 2.97% |
| 128 | 41/1280 | 3.20% |

Differences are last-bit float16, for example `0.9755859375` batched against `0.97607421875`
alone. The same shape holds at hidden 2560, the 4B's width.

A caution about how this was read at first. A single-seed run appeared to show a clean threshold at
32 rows, invariant below and dependent above. That is not true: other seeds show differences at 16
and none at 32. The effect is stochastic and data-dependent, which is why the table aggregates ten
seeds rather than reporting one draw. It would have been easy to publish the threshold.

The inputs are standard normal, not real activations, so the rate on production hidden states may
differ. What is established is that the dependence exists on the serving path, not its exact
frequency in production.

## How it fits the identity measurements

It supplies exactly the residue the all-reduce experiment could not remove, and the shape matches
what the ladders show:

- Below 16 rows the norm is invariant in this sample, and every route is exact at low concurrency.
- From 16 rows up a small fraction of rows carry a last-bit perturbation. A perturbation only
  changes a token when it lands on a near-tie, which is rare - so the result is the occasional lost
  request the ladders actually report (63/64, 95/96) rather than wholesale divergence.
- It explains why the one-card W4A16 route can be exact at 64 users in both passes and still miss
  one request at 96: the perturbation rate is roughly flat across those row counts while whether it
  matters depends on ties, which is not monotonic in batch size.

## What this does and does not change

It does not make the GEMM account wrong, and it does not show that the norm causes any specific
observed miss. Both would need more than this probe.

What it does change is the framing. Row-invariance has been treated as a property of the matmul, and
the W4A16 route's byte-exactness has been attributed to the kernel alone. On the same path there is
a second op that does not have the property. The right statement is that the INT4 route is exact in
the regimes measured, not that its kernel makes it exact everywhere - and the honest reason the
one-card route is byte-exact through 64 users is that the norm's perturbations happen not to land on
a tie there, not that nothing perturbs.

## Next

- A row-invariant variant of this norm is the obvious candidate fix, and it is cheaper to test than
  another collective variant because it reproduces on one card with no server.
- Re-run the probe with real activations captured from a decode step, to get a production rate.
- If a row-invariant norm exists, re-run the two-card ladder with it plus the row-wise all-reduce.
  The r0/r1 arms already show the all-reduce alone is not enough; the pair has not been tried.

Evidence: `data/2026-09-08-qwen35-rmsnorm-row-invariance-probe.json`.
