# The cross-card all-reduce is not by itself the two-card identity loss

> **Correction, 2026-09-08.** The reasoning below treats the control's `63/64` as a stable baseline.
> It is not: a third control arm, on a different overlay with its intervention switched off, later
> scored `64/64` in both passes. Six control passes now read four at `63/64` and two at `64/64`, so
> `r1`'s result sits inside the control distribution and this comparison never had the resolution to
> decide anything. The conclusion - that the row-wise all-reduce is not a demonstrated fix - stands,
> but for a stronger reason than the one given here. See
> [the intermittency note](2026-09-08-the-two-card-c64-identity-metric-is-intermittent.md).
>
> **Second correction, 2026-09-08.** Worse than underpowered: the intervention was never applied on
> the lane this note measures. The no-speculation ladder runs through `run-server.sh`, which did not
> forward `VLLM_XPU_ROWWISE_ALLREDUCE_MAX_ROWS` at all - only the speculative ladder received it. The
> `r1` container's `ladder-mtp0` environment has no such variable. So the c64 table below compares
> two identical configurations and establishes nothing about the row-wise all-reduce, in either
> direction. `run-server.sh` now forwards it, the campaign harness aborts if a requested knob is
> missing from the container, and the real arm is running as `q1`.

## What was being tested

On one card the Qwen3.5-9B W4A16 route matches its sequential oracle at every ladder rung through 64
users, in both passes. On two cards it scores 63/64 at 64 users, in both passes, and the 4B shows the
same shape - exact through 32 users, then losing requests. The GEMM under test is row-count invariant
by construction, so the arithmetic that varies has to be something the second card adds.

The Flash-Next lane had already established a mechanism that would explain it: XCCL's reduction order
depends on message size, so an `[M, N]` all-reduce does not agree bit for bit with `M` separate
`[1, N]` all-reduces. If that is what is happening, a decode step's result depends on how many rows
share it, and forcing every reduction onto the single-row path should restore identity.

## How

R276 does not carry that lane's row-wise communicator, so this used a diagnostic overlay: R276 plus
the row-wise all-reduce, pure Python, with no kernel, extension or device library touched. The
replaced communicator module was declared through `EXPECTED_XPU_COMMUNICATOR_SHA256`, which
`verify-image-contract.sh` already provides for candidates; every other pinned digest was re-verified
against the built image and the contract passes.

Two arms ran on that same image, so the rebuild itself is not the variable:

- **r0**, row-wise off - must reproduce the published control;
- **r1**, row-wise on for inputs of 2..64 rows.

## The control is sound

r0 reproduced R276 closely: `63/64` at 64 users in both passes at `2091.9`/`2093.0 tok/s`, against
the R276 control's `63/64` in both passes at `2083.7`/`2092.9`. The overlay changes nothing on its
own, which is what makes the second arm interpretable.

## Result: no, or at least not alone

| arm | 64 users, no speculation, pass 1 | pass 2 |
| --- | --- | --- |
| R276 control (campaign w3) | 63/64 at `2083.7` | 63/64 at `2092.9` |
| r0, row-wise off | 63/64 at `2091.9` | 63/64 at `2093.0` |
| r1, row-wise on | **64/64** at `2086.7` | 63/64 at `2088.2` |

One pass reached 64/64 and the other did not. That is a single request out of 64 in one pass of two,
against a control that scored 63/64 four times across two images - and, as the correction above
records, 64/64 twice on a third. It is not evidence that the row-wise path fixes anything, and it
should not be reported as a partial fix.

What it does establish is the negative: forcing every 2-to-64-row reduction onto exactly the path the
single-row step uses did **not** reliably restore identity. So the cross-card all-reduce is not by
itself the cause. Something else on the two-card path is also shape-dependent.

## What it costs, for whoever tries the next variant

~~Without speculation the row-wise path is nearly free at the rung that matters: `2086.7`/`2088.2`
tok/s against `2091.9`/`2093.0`, about `-0.25%`.~~ **Wrong, and wrong because the knob never reached
that container.** Applied and re-measured over 20 passes at 64 users, the row-wise path costs
`726.8` against `2088.1 tok/s` - **`-65.2%`**. A 65% loss is not a fix that could ship even if it
worked, which makes this a diagnostic rather than a candidate repair.

With MTP depth 3 it is severe, because the row count there is `users x (depth + 1)`, so the low rungs
sit under the threshold and pay `M` collectives on every step:

| users, depth 3 | row-wise off | row-wise on | delta |
| ---: | ---: | ---: | ---: |
| 8 | `938.4` | `398.9` | `-57%` |
| 16 | `974.7` | `406.4` | `-58%` |
| 32 | `1356.2` | `1200.9` | `-11%` (row count exceeds the threshold; path not taken) |

## The next suspect

The Flash-Next lane needed *two* row-wise switches, not one. The second
(`VLLM_XPU_ROWWISE_HC_NORM_MAX_ROWS`) exists because the mean in a grouped RMSNorm was also reduced
in a shape-dependent order - "a two-row batch differs from the same rows alone in about 1.5% of
random draws". That patch targets `vllm/models/qwen4_exp/amd/ops/hc.py`, a path Qwen3.5 does not use,
so it does not transfer directly. Its lesson does: on that lane the collective was one of at least
two shape-dependent reductions, and fixing only the collective was not enough there either.

Qwen3.5 runs its RMSNorm on the native path here (`VLLM_XPU_RMSNORM_TRITON=0`,
`VLLM_XPU_GEMMA_RMSNORM_TRITON=0`), and a norm whose reduction order varies with batch shape would
produce exactly this residue. That is the next thing to instrument, and it is cheaper to test than
another collective variant because it does not need a second card to reproduce - if the norm is
shape-dependent it should be visible on one card at the row counts where the two-card route fails.

Evidence: `data/2026-09-07-qwen35-9b-w4a16-tp2-rowwise-allreduce.json`; overlay in
`docker/r276-rowwise-allreduce-diag.Dockerfile` and `.patch`.
