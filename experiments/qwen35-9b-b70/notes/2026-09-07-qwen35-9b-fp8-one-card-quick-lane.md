# Qwen3.5-9B FP8-dynamic on one B70: quick lane (2026-09-07)

A "quick fun" lane after the 27B INT4 and Gemma 26B work: the smallest current Qwen3.5 dense-hybrid model, served
lossless-checked on one Arc Pro B70 with the lab's existing vLLM XPU stack, in one night, no new kernels.

## What ran

- Model: `RedHatAI/Qwen3.5-9B-FP8-dynamic`, revision `790f0576d2d77dd5322aa0603a470bd9e3a3d1f6` (compressed-tensors FP8
  per-channel weights, dynamic activations; hybrid linear-attention/full-attention layers like Qwen3.8; ships an MTP head
  `model_mtp.safetensors`). Pinned manifest: `manifests/model-direct-redhatai-qwen35-9b-fp8-dynamic-790f0576.json`
  (14.03 GB LFS). Downloaded with aria2 after the Gemma file (`scripts/download-…`).
- Stack: the published INT4-lane image (R276, `ghcr.io/steveseguin/vllm-openai-xpu-qwen38-int4@sha256:521eb277…`,
  vLLM 0.27.2rc1.dev77 XPU + lab kernels); its vLLM resolves `Qwen3_5ForConditionalGeneration` and offers the
  `qwen3_5_mtp` speculative method. Launched through the FP8 lane launchers (`repro/qwen38-27b-fp8-vllm-tp2-asrock-b70/
  run-w8a16-mtp1-server.sh`, `run-server.sh` for MTP0) with `QUANTIZATION=compressed-tensors VLLM_XPU_FP8_BLOCK_W8A16=0
  TENSOR_PARALLEL_SIZE=1 XPU_DEVICE_MASK=0 MAX_MODEL_LEN=8192 MAX_NUM_SEQS=16 MAX_NUM_BATCHED_TOKENS=2048`, strict env
  otherwise as the FP8 lane (`scripts/run-20260907-qwen35-9b-fp8-server.sh`).
- Workload: the lab's 12-prompt realistic suite over HTTP chat, 512 max tokens, cache zero, streamed token ids; metric =
  median tok/s over tokens 1-100 after TTFT (the Gemma/27B convention). One pass per configuration; boot 04:26-05:30 UTC.
- Identity: every response's token ids compared with the same-capture-mode no-speculation run.

## Results (one B70, tok/s)

| MTP depth | piecewise capture (size 1) | full decode-only capture (sizes 1-8) | identical to same-mode MTP0 |
| ---: | ---: | ---: | --- |
| 0 | 50.24 | 50.65 | - |
| 1 (eager, no capture) | 64.72 | - | 9/12 vs full, 7/12 vs piecewise (different compute path) |
| 1 | 75.94 | 77.19 | 12/12 |
| 2 | 92.04 | 94.59 | 12/12 |
| 3 | 103.16 | 105.30 (class-balanced 106.06, p10 89.6, full-512 83.2, TTFT 88 ms) | 12/12 |
| 4 | - | 109.88 (p10 87.7, full-512 82.8, TTFT 97 ms) | 11/12 |
| 5 | - | 110.09 (p10 84.7, full-512 77.9, TTFT 116 ms) | 11/12 |
| 6 | - | 109.00 (p10 79.6, full-512 72.3, TTFT 122 ms) | 11/12 |

All 12/12 responses valid and cache-zero in every run. Raw data: `data/qwen35-9b-fp8-smoke-20260907/<tag>/realistic-suite.json`.

## Reading it

- Speculation is the lever on this model: 50.6 -> 105.3 tok/s at depth 3 with byte-identical outputs, 2.08x. Capture mode
  matters little (+1-2%), unlike the 27B where full capture of the 10-20-token verify step was worth much more.
- Depths 4-6 gain 4% of median but lose p10 and the full-512 rate (longer answers accept fewer drafts late), raise TTFT, and
  one prompt diverges from the no-speculation oracle at every depth >= 4: the same near-tie mechanism seen on the 27B when
  the verify batch grows. Depth 3 is the lossless pick; depth 4 if the 4% matters more than the one near-tie.
- Compute-path identity: piecewise vs full capture vs eager disagree with each other on 4-5 of 12 prompts with no
  speculation involved, so "lossless" here means "identical to the same path without speculation", as in the other lanes.
- The chat template emits the model's thinking inline ("Thinking Process: ..."); the suite measured what streams, so the
  numbers are decode rates of the thinking+answer stream. A `chat_template_kwargs` thinking switch was not explored.

## Not done (this was a one-night pass)

Two-pass repeats, multi-user ladders, 32K context, a strict oracle pair, LocalMaxxing attestation, a package/recipe with
a pinned launcher. The wrappers under `scripts/` reproduce every row above from the pinned model and the R276 image.
