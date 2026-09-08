# Three candidates eliminated, none of them by spending cards

Follow-up to the finding that byte-identical prompts issued together return different completions.
The question was whether that tracks a request's slot in the batch or the scheduler drifting copies
into different decode steps. Neither, and a third candidate falls out on the way.

## Slot index does not predict it

Across both arms the minority-output slots are scattered - `050`, `054`, `024`, `026`, `001`, `038`
in one arm, an entirely different set in the other, nothing repeating more than three times out of
23 events. If a particular row position were arithmetically unlucky, the same slots would recur.
They do not.

## Step drift does not predict it either

Reconstructing absolute per-token arrival times from each request's start and its token offsets, the
spread across copies at the divergence index is **the same as the spread across copies that agree**:

| arm | spread at divergence | spread when agreeing |
| --- | ---: | ---: |
| `f0` | median `81.3 ms` | median `81.5 ms` |
| `f1` | median `255.4 ms` | median `254.9 ms` |

So divergence is not associated with unusual drift. What the numbers do show is that copies are
routinely spread over about **2.7 to 2.9 decode steps** whether or not they disagree - at `2093.6`
tok/s over 64 users a token takes roughly `31 ms`, and the median spread is `81 ms`. Copies of one
prompt are simply not in the same step, ever, which retires the tidy "same batch, different row"
framing the previous note offered as a possibility.

## The GEMM's fixed-K does cover the two-card shapes

The obvious remaining suspect was the matmul itself: tensor parallelism halves the projection shapes,
and if the fixed-K W4A16 strategy were gated on shapes it would stop applying on two cards, which
would explain one-card exactness and two-card divergence in one stroke.

It is not gated that way. Unlike the W8A16 patch, which carries an explicit five-shape production
whitelist, the W4A16 predicate is `(Ta_ext == u4 || s4) && Tb_ext == f16` with only an `n <= 1024`
bound. Sharded shapes stay inside it, both tiers were screened bitwise equal across TP1 and TP2
shapes for `n = 1..1024`, and so the GEMM remains row-count invariant on two cards. Eliminated
without a run.

## Where that leaves it

Ruled out at adequate power or by inspection: the cross-card all-reduce, the norm's variance
reduction, both together, slot position, step drift, and the GEMM's strategy selection. The
phenomenon itself is not in doubt - identical concurrent inputs return different outputs at about
`1.8%` on the prompts prone to it - but nothing tested so far accounts for it.

What has not been examined is everything between the projections: attention and the GDN recurrent
path have their own reductions over sequence and batch, and neither has been probed for row-count or
composition dependence the way the norm was. That probe is cheap - the norm one needed no server and
no second card - and it is the obvious next move rather than another intervention arm.

Evidence: `data/2026-09-08-copy-divergence-timing.json`; analyser
`scripts/analyze-copy-divergence-timing.py`.
