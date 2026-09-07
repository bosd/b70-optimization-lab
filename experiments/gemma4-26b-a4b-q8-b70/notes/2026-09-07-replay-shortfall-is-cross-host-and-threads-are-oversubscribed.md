# The Gemma replay shortfall is not run-to-run variance

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

## An easy 3%: the draft threads are oversubscribed here

The record passes `--spec-draft-threads 32 --spec-draft-threads-batch 32`. This host's CPU is an
8-core/16-thread EPYC 9015, so that asks for twice the hardware threads available. Dropping to 16
gains `3.06%` over the six-sample 32-thread mean; 8 gains `2.04%`. Both beat 32.

The more useful part is the spread. At 32 threads the six runs span `109.109`-`116.346` with a
`2.394%` CV; at 16 threads the two runs differ by `0.43%`. Oversubscription does not cap the peak -
the single best 32-thread run beat both 16-thread runs - it makes the typical run worse and the
lane harder to measure. With only two samples per thread setting the variance claim is suggestive
rather than settled, but the direction is consistent and the mechanism is not exotic.

This is a host-local tuning result. The four-card host has the cores to supply 32 draft threads, so
the record's setting is likely right there and wrong here.

## Separately: this lane does not reproduce its own answers

While comparing the runs it became clear that no two of them return the same text. Four fresh
servers, identical settings, identical prompt hashes, `temperature 0`, `top_p 1`, `seed 1` through
the chat API - and every pairwise comparison of the 12 outputs scores **0/12**, with divergence
starting as early as character 26.

The lane never claimed otherwise: its gates cover fresh-response validity, cache zero and canaries,
not output identity. So this is a previously unmeasured property, now measured, in
`data/2026-09-07-gemma4-q8-repeat-identity.json`.

One attribution caveat matters. The lane serves with speculative decoding, a Q4_0 MTP draft verified
by the Q8 target, and this measurement cannot separate a nondeterministic speculative path from a
nondeterministic target. A draftless arm would settle that and has not been run. What is established
is that the deployed configuration is not reproducible.

For scale, on the same host: the vLLM INT4 W4A16 route on Qwen3.5 is 12/12 across fresh servers, the
llama.cpp Q8 route on Qwen3.5-9B is 8/12, and this lane is 0/12. That is a third point on the same
curve rather than a surprise, and it is the strongest one yet for the claim that byte-identical
output is a property a stack has to be built for.

## Suggested follow-ups

- Record the hostname and CPU in `run_identity`. Establishing which machine set the record required
  counting GPU-index directory names, which is not a durable way to know.
- A draftless arm to attribute the 0/12 to the speculative path or the target.
- If this host is used for Gemma work again, run it at 16 draft threads.
