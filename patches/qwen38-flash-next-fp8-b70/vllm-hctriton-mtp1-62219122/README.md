# Qwen3.8 Flash-Next Triton hyper-connection glue on the placement MTP1 head (`62219122`)

Exported: 2026-09-07

The exact vLLM overlay of the Triton-HC line: one commit, `VLLM_XPU_HC_TRITON=1`
runs the model's Triton hyper-connection glue kernels (`_hc_gate_mix_kernel`,
`_hc_combine_kernel`, `_hc_combine_norm_kernel`, `_hc_silu_kernel` — the
reference path on CUDA) on XPU instead of the torch fallbacks the XPU port had
routed them to, on top of the certified placement MTP1 head `005dc578` (itself
nine commits over the lossless MTP1 head `1b2a17c1`, see
`../vllm-placement-mtp1-005dc578/`). The MoE kernel, the tuned map and the
placement are untouched; only `vllm/models/qwen4_exp/amd/ops/hc.py` changes.
The MTP0 twin of this series is `q38-placement-clean-v5-hc` at `8d7d6fd8` (the
same commit on `cb59004b`, tree `c2d3f962…`).

The Triton kernels round the mix/combine/norm glue differently from the torch
fallbacks at the last bf16 bit, so this line is a **new output authority**
(exact-2K `86b5b6c7…`, exact-4K `b89822ce…`, reproduced on fresh servers and
by the lossless MTP1 line), not a bit-identical continuation of the
torch-fallback authority `afffd211…` / `c6193cc6…`. The gate is opt-in: without
`VLLM_XPU_HC_TRITON=1` the head reproduces the placement line exactly.

- base: `005dc57895896f770157ea94f68e473e7447139e` (restore from the placement bundle first);
- head: `622191221475b53cc6f7f4d847860939f4c300ab`, tree `e79ab58bb96b807d4bebad5644bafa5e0d4327aa`;
- bundle `vllm-q38-hctriton-mtp1-62219122-20260907.bundle` carries tag `q38-hctriton-mtp1-62219122`;
- `series.sha256` pins the patch and the bundle; `verify-series.sh --apply` re-creates the tree.

| Patch | Subject |
| --- | --- |
| `0001-XPU-VLLM_XPU_HC_TRITON-1-run-the-Triton-hyper-connec.patch` | [XPU] VLLM_XPU_HC_TRITON=1: run the Triton hyper-connection glue kernels on XPU instead of the torch fallbacks |

```bash
REPRO_VLLM_TREE=/path/to/vllm-clone patches/qwen38-flash-next-fp8-b70/vllm-hctriton-mtp1-62219122/verify-series.sh --apply
```
