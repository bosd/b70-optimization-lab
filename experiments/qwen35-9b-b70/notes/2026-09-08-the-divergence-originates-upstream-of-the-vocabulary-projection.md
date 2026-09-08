# The divergence originates upstream of the vocabulary projection

## The test

The FP16 vocabulary projection is bitwise invariant to batch size at 32 decode rows and below and
row-dependent from 33 up - the only mechanism found whose threshold matches where the ladders break.
Chunking it to 32 rows was verified in-container to make every row's logits bitwise equal to its
single-row value, so unlike the serialised norm this candidate was value-preserving by construction.

Fragile-site suite, 20 passes at 64 users, 1280 requests per arm, same overlay image both sides, knob
presence checked in each container:

| arm | lm_head row chunk | divergent / 1280 | tok/s |
| --- | --- | ---: | ---: |
| `L0` | off | 22 (`1.72%`) | `2094.7` |
| `L1` | 32 | 20 (`1.56%`) | `2093.5` |

Two-sided binomial `p = 0.88`. No effect. The chunking is free - throughput is unchanged - and it does
not remove the divergence.

## What that rules in

This is the informative negative, because the intervention is known to work at what it targets. With
identical inputs, chunking makes the projection's output bitwise equal to the oracle's. The
divergences persist anyway. Therefore the inputs are not identical: **the hidden states arriving at
the vocabulary projection already differ between a concurrent request and the same request run
alone.**

That is the first positive localisation this line has produced, and it comes by elimination rather
than by probing. The cause is upstream, in the transformer body, not in the projection that reads its
output.

## The state of the search

Ruled out at adequate power or by construction: the cross-card all-reduce, the norm's variance
reduction, the two together, slot position, decode-step drift, the weight-quantised GEMM's strategy
selection, and now the vocabulary projection.

Established: the phenomenon is real and reproducible at about `1.7%` of requests on the prone prompts,
it resolves to a dozen fixed tie sites, and it originates before the head.

## What to do with that

The lab has bisected a model body before - R74 to R77 localised the Qwen3.8 c1/c2 difference to
`gdn_attention_core_xpu` in decoder layer 1 by comparing per-layer activations between arms. The same
method applies and is now well-targeted: capture the hidden state entering the head for a divergent
request and for its oracle, confirm they differ, then walk back through the layers to the first that
differs.

That is more work than a probe but it is the right shape of work: every remaining candidate inside
the body is cheaper to find by bisection than by guessing which op to make invariant next. Four
guesses have now been tested and none has moved the number.

Evidence: `data/2026-09-08-lmhead-chunk-identity.json`.
