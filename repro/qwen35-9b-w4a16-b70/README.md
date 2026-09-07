# Reproduce Qwen3.5 9B W4A16 with its own MTP head on one B70

> **Certification: `candidate-portable-repro`, not a starter guide.** Model
> revision, container image, launch chain and validation identities are pinned
> and were verified on the lab host on 2026-09-07. The remaining gates are a
> tested Intel driver/Docker installation path, beginner recovery guidance, and
> an independent clean-host replay. See the
> [guide catalog](../guide-catalog.json) and
> [certification standard](../../docs/reproduction-guide-certification.md).

RedHatAI's W4A16 quantization of Alibaba's Qwen3.5-9B (compressed-tensors INT4
weights, FP16 activations), served as published by vLLM XPU on one Intel Arc
Pro B70 through the lab's R276 image, with the publisher's MTP head as a
lossless speculative draft and full decode-only XPU graph capture. It is the
same stack, launcher and workload as the
[FP8 route](../qwen35-9b-fp8-b70/README.md) for the same model, so the two are
directly comparable.

## Headline (campaign w1, 2026-09-07, one B70)

- **MTP depth 3 with the draft-only INT4 lm_head: `113.627 / 112.904 tok/s`**
  class-balanced median decode over tokens 1-100 after TTFT on the strict
  12-prompt six-class completions suite, 512-token cap, cache zero, two fresh
  servers with separate empty compile caches. Median TTFT `68 ms`.
- **No speculation: `64.332 / 64.338 tok/s`** on the same suite.
- **Lossless:** G1 12/12 (the two MTP0 servers), G2 12/12 (the two depth-3
  servers), G3 12/12 twice (each depth-3 server against the MTP0 oracle);
  canaries passed on every server.
- LocalMaxxing: `cmtrhoyl1000cps01o43bhl72`, `113.265 tok/s`.
- ML Bottleneck's tuned-run target for `qwen3.5_9b` INT4 on one B70 is
  `99.12 tok/s`, physical ceiling `153.05`; the headline is 1.14x the target
  and 74% of the ceiling.

## Why this route also serves many users losslessly

vLLM's compressed-tensors path selects `CompressedTensorsWNA16`, which on XPU
is the lab's `wNa16` kernel (`_xpu_C.int4_gemm_w4a16`) carrying the fixed-K
two-tier W4A16 strategy built for the Qwen3.8 INT4 lane. That kernel does not
change its reduction order with the number of decode rows. The consequence is
visible in the identity ladders: without speculation this route is byte-exact
against a single request at **every rung through 64 users, in both passes**,
where the FP8 route on the same model, weights of the same publisher and the
same launcher flips a near-tie token from 16 users up.

| users | W4A16 tok/s (exact) | FP8 tok/s (exact) |
| ---: | ---: | ---: |
| 1 | 64.2 (1/1) | 50.1 (1/1) |
| 2 | 124.0 (2/2) | 97.2 (2/2) |
| 4 | 236.2 (4/4) | 187.5 (4/4) |
| 8 | 437.7 (8/8) | 355.0 (8/8) |
| 16 | 746.7 (16/16) | 634.7 (15/16) |
| 32 | 1184.0 (32/32) | 1055.2 (31/32) |
| 64 | **1268.4 (64/64)** | 1253.8 (59/64) |

No speculation, 128-token completions on the small-context suite, warm pass of
two, `max-model-len 256`, `max-num-seqs 64`. The identity ceiling is a property
of the kernel, not of the model or the workload.

The W4A16 determinism pad (`VLLM_XPU_W4A16_DETERMINISM_PAD`) is off in the
published configuration and should stay off. Measured on this model (campaign
w2): without speculation it is inert, because 64 users is 64 decode rows and
the pad only engages above 128, and the route is already exact there. With
depth 3 the verify step submits up to 256 rows, the pad engages, costs 13% at
64 users (683.7 against 789.2 tok/s) and changes nothing about identity
(62/64 against 61/64). The residual speculative flips above 16 users are
therefore not GEMM row-tier effects.

With MTP depth 3 the same ladder is exact through 16 users in both passes
(`750.8 tok/s`), 32/32 in the warm pass at `827.3` and 31/32 cold, and 61/64 at
`789.2`: the speculative verify step still walks through row counts the fixed-K
tiers do not cover.

## Model

Pinned in `manifests/model-direct-redhatai-qwen35-9b-w4a16-a398088c.json`:
`RedHatAI/Qwen3.5-9B-quantized.w4a16` at revision
`a398088c4228b0ae0c8c78df88fd1e4bf445f068`, three LFS files
(`model.safetensors` 10,952,xxx,xxx B, `model_mtp.safetensors` 486,582,848 B,
`tokenizer.json`) plus the small config files, 11.46 GB total. Download it the
same way as the FP8 route and keep the filenames; the launcher verifies every
LFS file against the manifest before the container starts.

## Launch

```bash
cd /path/to/b70-optimization-lab
MODEL_DIR=/models/Qwen3.5-9B-quantized.w4a16 VLLM_CACHE_DIR=/tmp/qwen35-w4a16-cache \
  repro/qwen35-9b-w4a16-b70/scripts/run-qwen35-9b-w4a16-server.sh
```

Every variable of the [FP8 launcher](../qwen35-9b-fp8-b70/README.md#launch)
applies unchanged: `MTP_DEPTH` (default 3), `TENSOR_PARALLEL_SIZE`,
`XPU_GRAPH`, `DRAFT_HEAD_INT4`, `PORT`, and the server-shape variables. The
image, kernel digests and determinism environment are identical, so the two
routes differ only in the weights on disk.

## Validate

Identical to the FP8 recipe: the strict suite with canaries, a depth-0 server
for the oracle, `compare-strict-attempt-outputs.py` for the 12/12 gate, and
`bench-openai-concurrency-oracle.py` for the identity ladder. See
[that section](../qwen35-9b-fp8-b70/README.md#validate) for the exact commands;
substitute this launcher and `qwen35-9b-w4a16-mtp3` as the served model name.

## Two cards (campaign w3, TP2)

Same launcher with `TENSOR_PARALLEL_SIZE=2`.

| measurement | one card | two cards |
| --- | ---: | ---: |
| no speculation, one user | 64.33 / 64.34 | 97.59 / 97.54 |
| MTP depth 3, one user | 113.63 / 112.90 | **172.27 / 172.32** |
| no speculation, exact ladder ceiling | 64 users, 1268.4 tok/s | 32 users, 1836.9 tok/s |
| depth 3, exact ladder ceiling | 16 users, 750.8 tok/s | 16 users, 1174.6 tok/s |

All strict gates pass 12/12 on both card counts. LocalMaxxing `cmtrn9hoy001ops01qzd4axry` at `172.296 tok/s`.

One difference is worth stating plainly: on one card this kernel is byte-exact at every rung through 64 users, and on
two cards 64 users drops to 63/64 in both passes while 32 users stays perfect. The kernel removes the variation that
comes from the number of decode rows; it cannot remove the variation that comes from summing partial results across two
cards. If byte-identical output at the largest batch matters more than aggregate throughput, one card is the safer
shape.

## Known limits

- Depth 4 and above were not run on this route; on the FP8 route they were
  repeat-exact but not lossless, and no faster.
- Two-card, graph-off and 2K-32K context rows exist for the FP8 route only.
- Not yet clean-host tested.
