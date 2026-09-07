# Qwen3.5-9B on two runtimes, one card, one suite (2026-09-07)

The lab serves this model through vLLM XPU in two quantizations. A Q8_0 GGUF of the same model was already on hand, so
this measures llama.cpp SYCL on the same card, the same strict 12-prompt completions suite and the same metric, to see
what the runtime choice is worth on its own.

## Setup

`unsloth/Qwen3.5-9B-GGUF` at revision `3885219b`, file `Qwen3.5-9B-Q8_0.gguf` (9,527,502,048 bytes,
sha256 `809626574d…`). The copy on this host arrived on an external drive; its digest matches the publisher revision
exactly, and the runner refuses to start if it does not. llama.cpp SYCL at `9fee29e`, AOT for `bmg-g31`, one B70,
`-ngl 99 -c 8192 -np 1 -b 1024 -ub 1024 -fa on -ctk f16 -ctv f16`, no speculation: this GGUF carries no MTP head, so
the honest comparison is against the vLLM no-speculation numbers. Two fresh servers, cache zero, workload gate passed
on both.

## Result

| runtime and weights | one user, tok/s | median TTFT | two fresh servers agree |
| --- | ---: | ---: | ---: |
| llama.cpp SYCL, Q8_0, no speculation | 47.24 / 48.86 | 247 ms | 8/12 |
| vLLM XPU, FP8-dynamic, no speculation | 50.18 / 50.15 | 54 ms | 12/12 |
| vLLM XPU, W4A16, no speculation | 64.33 / 64.34 | 48 ms | 12/12 |
| vLLM XPU, W4A16, MTP depth 3 | 113.63 / 112.90 | 68 ms | 12/12 |

vLLM with same-size INT4 weights is 1.34x faster than llama.cpp Q8 before speculation and 2.36x with the model's own
MTP head. First-token latency is about five times lower. Run-to-run speed also varies more on llama.cpp here: 3.4%
between two servers, against under 0.5% for every vLLM pair measured today.

## The part worth keeping

The two fresh llama.cpp servers agreed on only 8 of the 12 prompts (`incident-retrospective`, `code-review`,
`customer-email` and `sql-debugging` differed). That is a third independent case of the same effect: outputs that are
not reproducible between identical fresh servers, on a different runtime, a different quantization and a different
kernel stack from the two vLLM cases measured earlier the same day.

Collected, the picture is consistent. Byte-identical output across fresh servers and across batch sizes is not
something a stack has by default; on this hardware it is something the lab's row-invariant W4A16 INT4 kernel provides
and the alternatives do not:

| stack | repeat-exact across fresh servers |
| --- | --- |
| llama.cpp SYCL Q8_0 (9B) | no, 8/12 |
| vLLM FP8-dynamic (4B) | no, 11/12, 9/12, 11/12 over three pairs |
| vLLM FP8-dynamic (9B) | yes, but flips from 16 concurrent users |
| vLLM W4A16 INT4 (4B and 9B) | yes, and 9B stays exact to 64 concurrent users on one card |

Evidence: `data/2026-09-07-qwen35-9b-q8-llamacpp-comparison.json`, campaign root
`qwen35-9b-q8-llamacpp-tp1-20260907-g1`, runner `scripts/run-20260907-qwen35-9b-q8-llamacpp.sh`.

## Scope

One card, one suite, no speculation on the llama.cpp side because this GGUF has no draft head; unsloth publishes MTP
GGUFs for other sizes, so a speculative llama.cpp comparison is possible but was not run. Nothing here says llama.cpp
is slow in general: it says that on this card, for this model, the lab's vLLM stack is ahead on speed, latency and
reproducibility.
