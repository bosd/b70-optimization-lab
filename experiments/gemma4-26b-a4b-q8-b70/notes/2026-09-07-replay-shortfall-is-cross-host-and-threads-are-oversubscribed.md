# The Gemma replay shortfall is not run-to-run variance

> **Update, 2026-09-08.** The draft-thread result below did not survive confirmation. Four more
> runs at 16 threads took that arm to six samples, and the advantage fell from `3.06%` to `1.72%`
> with heavily overlapping ranges (Welch `t = 1.40`, about `p = 0.19`). It is not established. The
> cross-host finding, which is the substance of this note, is unaffected. See the section at the end.

The 2026-09-07 rebuild replays of the Gemma 4 26B A4B Q8 record landed at `111.197`, `116.346` and
`115.288 tok/s` against the promoted `124.977`. The recipe reads that as landing "within the known
several-percent spread". Three runs cannot separate a wide tail from a level shift, and the lane's
own documented repeatability is a `2.324%` run-median coefficient of variation with a `4.409%` p90
pairwise delta - smaller than the gap being explained. This adds five more runs and answers it.

Metric throughout is `median_tok_s_1_100_after_ttft`, the record's own metric. Every arm passed the
realistic gate, canaries 512/512, cache zero.

## The gap is systematic

| arm | n | mean | median | range | CV | % of record |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| record settings, 32 draft threads | 6 | `111.819` | `110.765` | `109.109`-`116.346` | `2.394%` | `89.47%` |
| 16 draft threads | 2 | `115.241` | `115.241` | `114.994`-`115.487` | `0.303%` | `92.21%` |
| 8 draft threads | 2 | `114.098` | `114.098` | `113.289`-`114.908` | `1.003%` | `91.30%` |
| host compatibility build, 32 threads | 1 | `115.288` | - | - | - | `92.25%` |

At the record's own settings the shortfall is `10.53%` on six samples whose coefficient of variation
is `2.394%`. The standard error of that mean is about `0.98%`, so the record sits roughly eleven
standard errors above it. The measured variance also matches the lane's documented `2.324%` almost
exactly, so this host is not noisier than recorded - it is centred lower. Even the best of the six
runs is `6.91%` short.

## Why: the record was set on the other host

The record-era Gemma runs in `data/` use four GPU indices: `645` runs on `gpu0`, `434` on `gpu1`,
`420` on `gpu2` and `404` on `gpu3`. This host has two B70s and can only address indices 0 and 1, so
that research ran on the four-B70 measuring host. The replays above ran here. The comparison was
therefore always cross-host, and `docs/model-effort-index.md` already records that the two hosts
differ in CPU, RAM and driver stack.

Nothing here says the record is wrong. It says a replay on this host is not the way to check it, and
that the recipe should not describe the difference as ordinary variance.

## The draft threads: a promising 3% that was not real

The record passes `--spec-draft-threads 32 --spec-draft-threads-batch 32`. This host's CPU is an
8-core/16-thread EPYC 9015, so that asks for twice the hardware threads available, and at two
samples per arm 16 threads looked `3.06%` faster with an eightfold tighter spread. That was worth
confirming before changing anything, so four more runs took the 16-thread arm to six samples.

It did not hold:

| arm | n | mean | range | CV |
| --- | ---: | ---: | --- | ---: |
| 32 draft threads | 6 | `111.819` | `109.109`-`116.346` | `2.394%` |
| 16 draft threads | 6 | `113.739` | `110.760`-`115.705` | `1.802%` |
| 8 draft threads | 2 | `114.098` | `113.289`-`114.908` | `1.003%` |

The advantage fell from `3.06%` to `1.72%`, the ranges overlap heavily, and a Welch t-test gives
`t = 1.40` on about `9.4` degrees of freedom, roughly `p = 0.19`. The tight `0.303%` spread that
made the two-sample result look decisive was itself the artifact: with six samples the 16-thread CV
is `1.802%`, not far below 32's `2.394%`.

So: **not established, and not a recipe change.** The direction is consistent across every
comparison and the oversubscription argument is physically reasonable, so it may well be a real
1-2% effect that six samples cannot resolve against this lane's noise. It is recorded here as a
lead, not a setting. Anyone wanting to settle it needs considerably more runs than this, and should
weigh that against a best case of about 2%.

## Separately: this lane does not reproduce its own answers

While comparing the runs it became clear that no two of them return the same text. Four fresh
servers, identical settings, identical prompt hashes, `temperature 0`, `top_p 1`, `seed 1` through
the chat API - and every pairwise comparison of the 12 outputs scores **0/12**, with divergence
starting as early as character 26.

The lane never claimed otherwise: its gates cover fresh-response validity, cache zero and canaries,
not output identity. So this is a previously unmeasured property, now measured, in
`data/2026-09-07-gemma4-q8-repeat-identity.json`.

The attribution is now settled. Two further servers ran the same gate with every `--spec-draft`
argument removed, so no drafting occurs at all: they score **0/12 against each other too**, diverging
as early as character 26. Removing speculation does not make the lane reproducible, so the
nondeterminism is in the target model's own decode path rather than in the draft or in draft
acceptance. Speculation is worth about `1.47x` here - `111.819` with the Q4_0 MTP draft against
`76.019` without - and it is not what costs the lane its reproducibility. Evidence:
`data/2026-09-08-gemma4-q8-draftless-repeat-identity.json`.

For scale, on the same host: the vLLM INT4 W4A16 route on Qwen3.5 is 12/12 across fresh servers, the
llama.cpp Q8 route on Qwen3.5-9B is 8/12, and this lane is 0/12. That is a third point on the same
curve rather than a surprise, and it is the strongest one yet for the claim that byte-identical
output is a property a stack has to be built for.

## Suggested follow-ups

- Record the hostname and CPU in `run_identity`. Establishing which machine set the record required
  counting GPU-index directory names, which is not a durable way to know.
- If this host is used for Gemma work again, run it at 16 draft threads.
