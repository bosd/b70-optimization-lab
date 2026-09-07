# Reproduce Qwen3.5 4B W4A16 with its own MTP head on one B70

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

## Known limits

- One card only; depths other than 0 and 3 were not run.
- No 2K-32K context ladder on this route yet.
- Not yet clean-host tested.
