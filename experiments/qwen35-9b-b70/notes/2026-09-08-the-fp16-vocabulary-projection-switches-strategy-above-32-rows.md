# The FP16 vocabulary projection switches strategy above 32 rows

The first mechanism found whose threshold matches where the ladders actually break.

## What was measured

The lab's fixed-K work made the weight-quantised projections invariant to decode row count. Its
predicate is `(Ta_ext == u4 || s4) && Tb_ext == f16` - weight-quantised only. On this route the target
verifier's `lm_head` is plain FP16 by design; only the draft head is INT4. So the last matmul before
the argmax, the one that actually decides a token, sits outside that coverage and had never been
checked.

Probed the same way as the norm - same rows alone and batched, compared bitwise, no server and no
second card:

| rows | rows differing from the same row alone | max abs logit delta |
| ---: | ---: | ---: |
| 2 - 32 | **0** | `0` |
| 33 | 99/99 (`100%`) | `3.906e-03` |
| 34, 36, 40, 44, 47, 48 | `100%` | `3.906e-03` |
| 64, 96, 128 | `100%` | `3.906e-03` |

A hard switch at 33 rows. At 32 and below the projection is bitwise identical whether a row is
computed alone or in a batch; from 33 up **every** row differs, by up to `3.9e-3` in logit space.
Both the TP1 vocabulary and the TP2 shard behave identically, so the shard width is not the trigger -
the row count is.

## Why this is the interesting one

It is the only mechanism found so far whose threshold lines up with the observed behaviour. The
concurrency ladders are exact at 32 users on both topologies and lose requests above: two cards at
64, one card at 96. Below 33 rows this projection cannot contribute a difference at all; above it,
every row's logits move.

It also explains why the interventions failed. The row-wise all-reduce and the serialised norm both
made their own arithmetic invariant to row count, and neither touched this GEMM - so the largest
row-count-dependent perturbation in the model, sitting directly before the argmax, was left in place
in every arm including the control.

## What it does not establish

The probe uses random weights and activations, whose logit margins are enormous, so the argmax never
moved in the sample. That is expected and is not evidence against the mechanism: a `3.9e-3` shift
only changes a token when the top two candidates are within that of each other, which is precisely
the near-tie condition the divergences show. Demonstrating that these shifts cause the observed flips
needs an intervention, not another probe.

It also does not explain the difference between one and two cards on its own, since both share the
threshold. The natural reading is that this projection supplies the perturbation on both topologies
and two cards are more fragile at the same row count, but that is a hypothesis.

## The concrete next step

Extend the fixed-K treatment to the FP16 head, or pad the head's decode rows to tiers of 32 or fewer.
Either restores invariance in the one place where a last-bit change can flip a token, and unlike the
serialised norm it is targeting an op that demonstrably changes behaviour exactly where the ladders
change behaviour. Then re-run the fragile-site arms, which now have enough power to decide it: the
control yields 23 events per 1280 requests.

Evidence: `data/2026-09-08-lm-head-row-invariance.json`; probe
`probes/lm-head-gemm-row-invariance.py`.
