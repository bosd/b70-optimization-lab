# Qwen3.5 9B W4A16 — one-B70 package (candidate)

RedHatAI's W4A16 quantization of Qwen3.5-9B (compressed-tensors INT4 weights, FP16 activations) served by vLLM XPU on a
single Intel Arc Pro B70 32 GiB card, with the publisher's own MTP head as a lossless speculative draft and full
decode-only XPU graph capture. The container image and the strict launcher chain are the Qwen3.8 lanes', unchanged.

> **Single request (2026-09-07, campaign w1):** MTP depth 3 with the draft-only INT4 lm_head `113.63 / 112.90 tok/s`,
> no speculation `64.33 / 64.34` (two fresh servers each, class-balanced median decode on the strict 12-prompt suite).
> Both speculative servers matched each other and the no-speculation oracle on all 12 complete token arrays, so the
> speedup is lossless. LocalMaxxing `cmtrhoyl1000cps01o43bhl72` at `113.265 tok/s`.

> **Concurrent users (c1-c64 identity ladder, 128 tokens per request):** without speculation this route is
> byte-identical to a single request at **every rung through 64 users, in both passes** (`1268.4 tok/s` at 64 users,
> 64/64), which is what the FP8 build of the same model cannot do. With depth 3 it is exact through 16 users
> (`750.8 tok/s`); 32 and 64 users are measured and withheld.

> **Long context:** not measured on this route yet; the FP8 route's 2K-32K ladder is in
> `repro/qwen35-9b-fp8-b70/README.md`.

## Why this route rather than FP8

The same publisher's FP8-dynamic build of this model is packaged separately and is slower at every depth, but the real
difference is reproducibility. vLLM's compressed-tensors path selects `CompressedTensorsWNA16`, which on XPU is the
lab's `wNa16` kernel with the fixed-K two-tier W4A16 strategy. That kernel does not vary its reduction order with the
number of decode rows, so a token whose top two candidates are exactly tied resolves the same way no matter how many
requests share the step. The FP8 path has no such guarantee and flips a handful of prompts from 16 users up.

The determinism pad (`VLLM_XPU_W4A16_DETERMINISM_PAD`) is off and should stay off: measured on this model it is inert
below its 128-row threshold and costs 13% at 64 users above it, buying no identity.

## Commands

```bash
# image (public, anonymous pull verified 2026-09-07 by tag and digest)
docker pull ghcr.io/steveseguin/vllm-openai-xpu-qwen38-int4@sha256:521eb277c0733f8c2ce47aea1bb98ed576c6f1ad63bf5baf22d38fc07abf54ad
docker tag  ghcr.io/steveseguin/vllm-openai-xpu-qwen38-int4@sha256:521eb277c0733f8c2ce47aea1bb98ed576c6f1ad63bf5baf22d38fc07abf54ad \
            neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276

# serve (MTP_DEPTH=0 for the no-speculation profile)
MODEL_DIR=/models/Qwen3.5-9B-quantized.w4a16 VLLM_CACHE_DIR=/tmp/qwen35-w4a16-cache MTP_DEPTH=3 \
  repro/qwen35-9b-w4a16-b70/scripts/run-qwen35-9b-w4a16-server.sh

# strict benchmark with canaries
OUT_DIR=/tmp/strict-a BASE_URL=http://127.0.0.1:18131 MODEL_NAME=qwen35-9b-w4a16-mtp3 \
  repro/qwen38-27b-fp8-vllm-tp2-asrock-b70/bench-w8a16-mtp1-strict.sh
```

Full procedure, validation commands and the identity tables: [`repro/qwen35-9b-w4a16-b70/README.md`](../../repro/qwen35-9b-w4a16-b70/README.md).

## Still missing

- clean-host replay
- two-card, graph-off and 2K-32K rows (measured on the FP8 route only)
