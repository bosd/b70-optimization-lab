# Qwen3.5 4B W4A16 — one-B70 package (candidate)

RedHatAI's W4A16 quantization of Qwen3.5-4B (compressed-tensors INT4 weights, FP16 activations) served by vLLM XPU on a
single Intel Arc Pro B70, with the publisher's MTP head as a lossless speculative draft and full decode-only XPU graph
capture. Same image, launcher and gates as the 9B INT4 package; only the weights differ.

> **Single request (2026-09-07, campaign v1):** MTP depth 3 with the draft-only INT4 lm_head `177.41 / 177.17 tok/s`,
> no speculation `102.63 / 102.38` (two fresh servers each, class-balanced median decode on the strict 12-prompt
> suite). Every gate exact: the two speculative servers matched each other and both matched the no-speculation oracle
> on all 12 complete token arrays. LocalMaxxing `cmtrj2tp3000hps01n3fadg9d` at `177.287 tok/s`.

> **Concurrent users (c1-c64 identity ladder, 128 tokens per request):** without speculation, byte-identical to a
> single request at every rung through 32 users in both passes (`1593.9 tok/s`); 64 users reaches `1725.1` but flipped
> one answer in one pass, so it is withheld. With depth 3, exact through 16 users (`1089.9 tok/s`).

## Why the FP8 build of this model is not packaged

It cannot pass the base identity gate on this stack. Three independent pairs of fresh servers, one user each, nothing
concurrent, agreed on only 11/12, 9/12 and 11/12 of the twelve prompts. Three prompts are tie-prone and each has
exactly two valid continuations, with servers picking independently: an exact tie in the next-token scores resolved by
per-process state. On the INT4 kernel the same gate passes 12/12. The evidence is kept in
[`experiments/qwen35-4b-b70/notes/2026-09-07-qwen35-4b-fp8-not-repeat-exact.md`](../../experiments/qwen35-4b-b70/notes/2026-09-07-qwen35-4b-fp8-not-repeat-exact.md)
rather than discarded, because it is half of the evidence that the identity ceiling is a property of the kernel.

## Commands

```bash
docker pull ghcr.io/steveseguin/vllm-openai-xpu-qwen38-int4@sha256:521eb277c0733f8c2ce47aea1bb98ed576c6f1ad63bf5baf22d38fc07abf54ad
docker tag  ghcr.io/steveseguin/vllm-openai-xpu-qwen38-int4@sha256:521eb277c0733f8c2ce47aea1bb98ed576c6f1ad63bf5baf22d38fc07abf54ad \
            neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276

MODEL_DIR=/models/Qwen3.5-4B-quantized.w4a16 VLLM_CACHE_DIR=/tmp/qwen35-4b-cache MTP_DEPTH=3 \
  repro/qwen35-4b-w4a16-b70/scripts/run-qwen35-4b-w4a16-server.sh
```

Full procedure and validation: [`repro/qwen35-4b-w4a16-b70/README.md`](../../repro/qwen35-4b-w4a16-b70/README.md).

## Still missing

- clean-host replay
- 2K-32K context rows
