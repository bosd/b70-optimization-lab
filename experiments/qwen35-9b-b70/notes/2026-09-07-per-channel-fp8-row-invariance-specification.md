# What a row-invariant per-channel FP8 GEMM would take (specified, not built)

The FP8 routes carry three open negative results that all have the same shape: the Qwen3.5-4B FP8
build is not repeat-exact across fresh servers (11/12, 9/12, 11/12 over three pairs), the 9B FP8
build is repeat-exact at one user but flips a near-tie token from 16 users up, and neither route has
a concurrency identity claim. The W4A16 route on the same models, same publisher and same launcher
passes all of it. One change would close all three: make the FP8 GEMM's reduction independent of the
row count, the way the W4A16 kernel already is.

This note records what that change actually involves, because the answer is not "extend the existing
fixed-K patch" and the difference matters for whoever picks it up.

## The existing row-invariance work does not cover these checkpoints

`experiments/qwen38-27b-b70/patches/onednn-qwen38-w8a16-fixed-k-align16-r137a-20260902.patch`
pins the K partition for FP8 weights, and it is guarded by:

```
problem.Ta_ext == Type::hf8 && problem.Ta == Type::hf8
&& problem.Ta_scale == Type::f32 && problem.aScale2D()
&& problem.aqGroupM == 128 && problem.aqGroupK == 128
```

plus a whitelist of five Qwen3.8-27B shapes and `n <= 512`. That is **block-scaled** FP8: a 2D grid
of 128x128 scales.

The RedHatAI Qwen3.5 checkpoints are not block-scaled. From their `config.json`:

| checkpoint | weights | activations |
| --- | --- | --- |
| `Qwen3.5-9B-FP8-dynamic` | `float`, 8 bits, `strategy=channel` | `float`, 8 bits, `strategy=token`, dynamic |
| `Qwen3.5-4B-FP8-dynamic` | same | same |
| `Qwen3.5-9B-quantized.w4a16` | `int`, 4 bits, `strategy=group`, group 128 | none |

Per-channel weight scales are one scale per output channel, so `aScale2D()` is false and the
`aqGroupM/aqGroupK == 128` test cannot hold. The predicate never fires, the catalog picks the
strategy, and the catalog varies its K partition with the row count. That is the row dependence.

Two consequences worth stating plainly:

- The per-token dynamic **activation** scale is not the problem. Each token's scale depends only on
  that token, so it is already row-invariant. The weight-side reduction is what varies.
- `VLLM_XPU_W8A16_DECODE_PAD_ROWS` is not a shortcut here. Padding rows to a fixed tier would give
  the GEMM a constant M, but the R118 patch that implements it is **not in the R276 image** (the
  string does not appear in `scaled_mm/xpu.py` there), and it targets `fp8_gemm_w8a16`, the
  block-scaled path, not the per-channel one. The launcher forwards the variable, so it is set to 0
  in every published Qwen3.5 result and does nothing at all in this image. That is worth knowing
  before someone reads it as an active knob.

## What the extension has to do

1. Add a predicate branch for per-channel FP8: `Ta_ext == hf8` with a 1D weight scale, rather than
   `aScale2D()` with 128x128 grouping.
2. Widen the shape guard. The current whitelist is five Qwen3.8-27B `(m, k)` pairs. The Qwen3.5
   projections are, with `m` the output features:

   | model | qkv | o | gate_up | down |
   | --- | --- | --- | --- | --- |
   | 9B (hidden 4096, inter 12288) | (6144, 4096) | (4096, 4096) | (24576, 4096) | (4096, 12288) |
   | 4B (hidden 2560, inter 9216) | (6144, 2560) | (2560, 4096) | (18432, 2560) | (2560, 9216) |

   Both models are 32 layers, 16 heads, 4 KV heads, head dim 256, vocab 248320.
3. Find and validate fixed strategy strings for those shapes, the way R220/R221 did for W4A16:
   screen candidates for bitwise equality across the whole row range before pinning, rather than
   picking the fastest.
4. Rebuild oneDNN and the image, then re-run the strict pairs and the ladders.

Step 3 is the real work and it is the step that cannot be skipped: the W4A16 two-tier selection was
only adopted after both tiers were screened bitwise equal on all 14 TP1/TP2 shapes for n = 1..1024.

## Why this was not built in this session

Steps 3 and 4 need the cards and a oneDNN rebuild, and the cards were committed to the two-card
identity experiment, the c128 ladder, and the Gemma replay distribution. Nothing above is a
measurement; it is a specification with the guard conditions and shapes filled in so the next
session does not have to rediscover that the existing FP8 fixed-K patch does not apply.
