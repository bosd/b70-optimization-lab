# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `5`.
- Route mode/source: `synthetic_hot_skew`.
- Quant out-variant available: `True`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `142.000`.
- Fused-prologue offset-GEMM max abs diff: `142.000`.
- Full C++ layerlet max abs diff: `142.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `142.000`.
- Rows-per-expert INT8 oracle max abs diff versus BF16 dequantized reference: `2.000`.

## Timing

- Mean `xpu_fused_moe`: `330.468 us`.
- Mean scratch `xpu_fused_moe`: `267.107 us`.
- Mean preallocated staged: `209.041 us`.
- Mean fused-prologue staged: `289.749 us`.
- Mean fused-prologue offset-GEMM staged: `212.231 us`.
- Mean full C++ layerlet: `183.777 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | None | 8 | 355.729 | 295.149 | 233.285 | 330.473 | 238.397 | n/a | n/a | 194.691 | 112.801 | 109.453 | 202.943 |
| 2 | None | 12 | 323.193 | 253.481 | 197.005 | 273.959 | 202.130 | n/a | n/a | 201.058 | 95.365 | 95.079 | 166.355 |
| 4 | None | 14 | 317.769 | 263.214 | 204.584 | 280.316 | 205.010 | n/a | n/a | 171.915 | 98.670 | 100.061 | 177.005 |
| 8 | None | 16 | 305.279 | 244.601 | 190.892 | 266.737 | 197.038 | n/a | n/a | 166.761 | 94.549 | 95.124 | 165.175 |
| 16 | None | 16 | 350.370 | 279.090 | 219.440 | 297.261 | 218.579 | n/a | n/a | 184.460 | 104.153 | 103.665 | 181.935 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `5`.
- Best exact non-reference full-layerlet candidate: `preallocated_staged` at `190.892 us` (`1.599x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | None | full_layerlet | 194.691 | 1.827 | False | best_exact_nonreference_misses_target_layerlet_us |
| 2 | None | preallocated_staged | 197.005 | 1.641 | False | best_exact_nonreference_misses_target_layerlet_us |
| 4 | None | preallocated_staged | 204.584 | 1.553 | False | best_exact_nonreference_misses_target_layerlet_us |
| 8 | None | preallocated_staged | 190.892 | 1.599 | False | best_exact_nonreference_misses_target_layerlet_us |
| 16 | None | preallocated_staged | 219.440 | 1.597 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is not exact against `xpu_fused_moe`; do not use it as an endpoint candidate.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
