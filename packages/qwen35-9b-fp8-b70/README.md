# Qwen3.5 9B FP8-dynamic — one-B70 package (candidate)

RedHatAI's FP8-dynamic quantization of Qwen3.5-9B (compressed-tensors per-channel FP8 weights, dynamic activations)
served by vLLM XPU on Intel Arc Pro B70 cards, with the publisher's MTP head as a lossless speculative draft.

> **Prefer the INT4 build on this hardware.** [`qwen35-9b-w4a16-b70`](../qwen35-9b-w4a16-b70/README.md) is the same
> model from the same publisher, is faster at every depth (`113.6` against `98.3 tok/s` at depth 3), and stays
> byte-identical to a single request at every concurrency through 64 users, where this route flips a near-tie token
> from 16 users up. This package remains published because its numbers are real and because the pair is the evidence
> that the identity ceiling comes from the kernel rather than the model.

> **Single request (2026-09-07):** one card, MTP depth 3 with the draft-only INT4 lm_head `98.25 / 98.03 tok/s`, no
> speculation `50.17 / 50.15`; two cards, depth 3 `147.71 / 147.89`, no speculation `79.46 / 79.40`. Every pair matched
> its sibling and the no-speculation oracle on all 12 complete token arrays. LocalMaxxing
> `cmtqyanxc00bjpa01nojy87wp` (one card) and `cmtqzhlvn00c0pa0109xxfb2f` (two cards).

> **Concurrent users:** exact through 8 users on one card (`564.7 tok/s`) and 8 on two cards (`848.7`); higher rungs
> are measured and withheld because near-tie prompts diverge.

> **Long context:** 2K to 32K on real unrepeated content, every answer identical to the no-speculation oracle at every
> depth (18/18 on each card count): `86.8 tok/s` at 32K on one card, `140.6` on two.

## Depth guidance

Depth 4 and beyond are repeat-exact but not lossless on this route (8/12 and 9/12 against the oracle) and no faster, so
depth 3 is the published setting. Depths 5 and 6 are slower still.

## Commands

```bash
docker pull ghcr.io/steveseguin/vllm-openai-xpu-qwen38-int4@sha256:521eb277c0733f8c2ce47aea1bb98ed576c6f1ad63bf5baf22d38fc07abf54ad
docker tag  ghcr.io/steveseguin/vllm-openai-xpu-qwen38-int4@sha256:521eb277c0733f8c2ce47aea1bb98ed576c6f1ad63bf5baf22d38fc07abf54ad \
            neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276

MODEL_DIR=/models/Qwen3.5-9B-FP8-dynamic VLLM_CACHE_DIR=/tmp/qwen35-cache MTP_DEPTH=3 \
  repro/qwen35-9b-fp8-b70/scripts/run-qwen35-9b-fp8-server.sh   # TENSOR_PARALLEL_SIZE=2 for the two-card profile
```

Full procedure, matrix and validation: [`repro/qwen35-9b-fp8-b70/README.md`](../../repro/qwen35-9b-fp8-b70/README.md).

## Still missing

- clean-host replay
