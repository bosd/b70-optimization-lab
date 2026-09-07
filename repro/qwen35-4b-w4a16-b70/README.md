# Reproduce Qwen3.5 4B W4A16 with its own MTP head on one or two B70s

> **Certification: `candidate-portable-repro`, not a starter guide.** Model
> revision, container image, launch chain and validation identities are pinned
> and were verified on the lab host on 2026-09-07. The remaining gates are a
> tested Intel driver/Docker installation path, beginner recovery guidance, and
> an independent clean-host replay. See the
> [guide catalog](../guide-catalog.json) and
> [certification standard](../../docs/reproduction-guide-certification.md).

RedHatAI's W4A16 quantization of Alibaba's Qwen3.5-4B (compressed-tensors INT4
weights, FP16 activations), served as published by vLLM XPU on one Intel Arc
Pro B70 through the lab's R276 image, with the publisher's MTP head as a
lossless speculative draft and full decode-only XPU graph capture. It is the
same stack and launcher as the
[9B W4A16 route](../qwen35-9b-w4a16-b70/README.md); only the weights differ.

## Headline (campaign v1, 2026-09-07, one B70)

- **MTP depth 3 with the draft-only INT4 lm_head: `177.406 / 177.168 tok/s`**
  class-balanced median decode over tokens 1-100 after TTFT on the strict
  12-prompt six-class completions suite, 512-token cap, cache zero, two fresh
  servers with separate empty compile caches. Median TTFT `45 ms`.
- **No speculation: `102.625 / 102.376 tok/s`** on the same suite.
- **Lossless:** G1, G2 and both G3 comparisons matched 12/12 complete token
  arrays; canaries passed on every server.
- LocalMaxxing: `cmtrj2tp3000hps01n3fadg9d`, `177.287 tok/s`.

## Two cards (campaign t1, TP2)

A 4B model is small enough that the second card could plausibly cost more in collective traffic than it returns. It
does not: the second card is worth more to this model than to the 9B.

| measurement | one card | two cards |
| --- | ---: | ---: |
| no speculation | 102.63 / 102.38 | **138.17 / 138.06** |
| MTP depth 3, one user | 177.41 / 177.17 | **240.62 / 227.53** |
| 32 users, no speculation | 1593.9 (32/32) | **2342.9 / 2353.9 (32/32)** |
| 64 users, no speculation | 1725.1 (63/64) | **2752.6 / 2777.7 (62/64, 64/64)** |

All strict gates pass 12/12 on both card counts, and the two two-card depth-3 servers returned byte-identical answers
on all 12 prompts.

Two caveats belong with those numbers. The two-card depth-3 pair measured `240.615` and `227.533 tok/s`, a `5.8%`
spread, where the one-card pair of the same lane differed by `0.13%`; two-card speculative decode is markedly noisier
here, so its center is quoted with that spread rather than as a tight figure. And concurrency identity is weaker on
two cards: without speculation the route is exact through 32 users in both passes but scores 62/64 then 64/64 at 64
users, and with depth 3 it is exact only through 16. The 9B on this same kernel is exact at every rung through 64
users on one card and drops to 63/64 on two, so on both models the loss appears when the second card joins. That
points at the cross-card reduction rather than the GEMM.

## Why this route and not the FP8 one

The FP8-dynamic build of the same model **cannot pass the base identity gate on
this stack**. Three independent fresh-server pairs scored 11/12, 9/12 and 11/12:
three of the twelve prompts are tie-prone, each with exactly two valid
continuations, and servers pick between them independently
(`../../experiments/qwen35-4b-b70/notes/2026-09-07-qwen35-4b-fp8-not-repeat-exact.md`).

On this route the same gate passes **12/12**. The difference is the kernel:
vLLM's compressed-tensors path selects `CompressedTensorsWNA16`, which on XPU is
the lab's `wNa16` kernel (`_xpu_C.int4_gemm_w4a16`) with the fixed-K two-tier
strategy, and that kernel does not vary its reduction order. The 9B shows the
same effect in its own way: there the FP8 route is repeat-exact but flips at
concurrency, and the W4A16 route is byte-exact at every rung through 64 users.
Two models, two different symptoms, one cause and one fix.

## Model

Pinned in `manifests/model-direct-redhatai-qwen35-4b-w4a16-7a613872.json`:
`RedHatAI/Qwen3.5-4B-quantized.w4a16` at revision
`7a613872f394578b0b52b683ff4ac47516b4bcaf`, 5.54 GB across three LFS files
including the `model_mtp.safetensors` draft head. The launcher verifies every
LFS file against the manifest before the container starts.

## Launch

```bash
cd /path/to/b70-optimization-lab
MODEL_DIR=/models/Qwen3.5-4B-quantized.w4a16 VLLM_CACHE_DIR=/tmp/qwen35-4b-cache \
  repro/qwen35-4b-w4a16-b70/scripts/run-qwen35-4b-w4a16-server.sh
```

Every variable of the [shared launcher](../qwen35-9b-fp8-b70/README.md#launch)
applies unchanged: `MTP_DEPTH` (default 3), `TENSOR_PARALLEL_SIZE`, `XPU_GRAPH`,
`DRAFT_HEAD_INT4`, `PORT` and the server-shape variables.

## Validate

Identical to the 9B recipes: the strict suite with canaries, a depth-0 server
for the oracle, `compare-strict-attempt-outputs.py` for the 12/12 gate, and
`bench-openai-concurrency-oracle.py` for the identity ladder. Substitute this
launcher and `qwen35-4b-w4a16-mtp3` as the served model name.

## Many users (campaign v1, one B70, warm pass of two)

| users | no speculation tok/s (exact) | depth 3 + INT4 draft head tok/s (exact) |
| ---: | ---: | ---: |
| 1 | 101.9 (1/1) | 159.2 (1/1) |
| 2 | 193.5 (2/2) | 300.8 (2/2) |
| 4 | 362.3 (4/4) | 537.8 (4/4) |
| 8 | 655.5 (8/8) | 898.0 (8/8) |
| 16 | 1059.3 (16/16) | 1089.9 (16/16) |
| 32 | 1593.9 (32/32) | 1147.4 (30/32) |
| 64 | 1725.1 (63/64) | 1201.0 (55/64) |

128-token completions on the small-context suite, `max-model-len 256`,
`max-num-seqs 64`. Without speculation every rung through 32 users is exact in
both passes; depth 3 is exact through 16 and is the faster choice up to that
point, after which plain decoding wins.

## Long context: 2K to 32K real content (campaign v2)

One slot, unrepeated real content (three requests per depth, median shown), 128 output tokens, cache zero, canaries
before and after; the depth-3 arm ran against a same-configuration MTP0 arm as its oracle.

| active context | no speculation tok/s | depth 3 + INT4 draft head tok/s (exact vs oracle) |
| ---: | ---: | ---: |
| 2,048 | 99.6 | 177.0 (3/3) |
| 4,096 | 98.1 | 188.3 (3/3) |
| 8,192 | 95.7 | 188.8 (3/3) |
| 16,384 | 91.6 | 191.6 (3/3) |
| 24,576 | 87.8 | 161.5 (3/3) |
| 32,768 | 84.4 | 149.9 (3/3) |

All 18 depth-3 answers matched the oracle. This model holds its speed at length better than the 9B, which falls to
89.5 tok/s at 32K against this one's 149.9.

## Known limits

- Depths other than 0 and 3 were not run.
- Two-card concurrency identity is not qualified above 32 users without
  speculation, or above 16 with it.
- Not yet clean-host tested.
