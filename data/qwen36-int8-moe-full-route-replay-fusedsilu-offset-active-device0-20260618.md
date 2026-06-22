# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `True`.
- TP size: `4`.
- Result rows: `16`.
- Quant out-variant available: `True`.
- Route source: `data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Fused-prologue active-offset-GEMM max abs diff: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `319.214 us`.
- Mean scratch `xpu_fused_moe`: `267.063 us`.
- Mean preallocated staged: `217.882 us`.
- Mean fused-prologue staged: `292.374 us`.
- Mean fused-prologue offset-GEMM staged: `213.448 us`.
- Mean fused-prologue active-offset-GEMM staged: `216.120 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 296.097 | 252.415 | 207.737 | 277.819 | 198.867 | 202.511 | 95.531 | 94.980 | 173.040 |
| 1 | 4 | 8 | 304.772 | 256.819 | 209.383 | 283.097 | 205.485 | 209.075 | 100.237 | 99.975 | 176.852 |
| 1 | 8 | 8 | 349.587 | 295.929 | 242.388 | 321.336 | 235.475 | 235.198 | 116.230 | 112.573 | 199.481 |
| 1 | 12 | 8 | 295.433 | 245.532 | 200.729 | 270.618 | 196.702 | 198.780 | 97.739 | 96.547 | 169.357 |
| 1 | 16 | 8 | 369.051 | 310.525 | 255.417 | 339.290 | 246.470 | 252.210 | 118.459 | 119.609 | 210.392 |
| 1 | 20 | 8 | 283.457 | 236.298 | 194.040 | 260.026 | 189.774 | 193.194 | 93.104 | 92.848 | 165.467 |
| 1 | 24 | 8 | 300.820 | 255.452 | 205.939 | 272.643 | 201.528 | 202.360 | 97.068 | 97.873 | 172.994 |
| 1 | 28 | 8 | 378.940 | 303.172 | 242.899 | 335.480 | 242.774 | 248.220 | 120.770 | 119.808 | 222.518 |
| 1 | 32 | 8 | 295.989 | 250.716 | 204.844 | 273.534 | 201.757 | 205.081 | 98.036 | 97.181 | 172.281 |
| 1 | 36 | 8 | 309.741 | 259.896 | 211.976 | 287.120 | 206.551 | 214.124 | 102.204 | 102.778 | 176.767 |
| 1 | 40 | 8 | 311.270 | 266.380 | 217.776 | 291.649 | 217.747 | 214.048 | 102.189 | 103.201 | 180.111 |
| 1 | 44 | 8 | 360.263 | 292.607 | 239.006 | 322.301 | 239.313 | 238.827 | 121.065 | 119.028 | 209.576 |
| 1 | 48 | 8 | 293.959 | 245.880 | 201.063 | 269.883 | 198.787 | 201.261 | 96.571 | 96.328 | 172.018 |
| 1 | 52 | 8 | 294.797 | 252.122 | 203.946 | 277.335 | 201.023 | 202.323 | 97.032 | 96.290 | 171.305 |
| 1 | 56 | 8 | 310.140 | 263.423 | 218.137 | 286.664 | 206.915 | 211.682 | 102.339 | 101.291 | 178.807 |
| 1 | 60 | 8 | 353.101 | 285.837 | 230.830 | 309.183 | 225.997 | 229.027 | 114.431 | 110.958 | 195.957 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `16`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `189.774 us` (`1.494x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_offset_gemm | 198.867 | 1.489 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | fused_prologue_offset_gemm | 205.485 | 1.483 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | fused_prologue_active_offset_gemm | 235.198 | 1.486 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | fused_prologue_offset_gemm | 196.702 | 1.502 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | fused_prologue_offset_gemm | 246.470 | 1.497 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | fused_prologue_offset_gemm | 189.774 | 1.494 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | fused_prologue_offset_gemm | 201.528 | 1.493 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | fused_prologue_offset_gemm | 242.774 | 1.561 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | fused_prologue_offset_gemm | 201.757 | 1.467 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | fused_prologue_offset_gemm | 206.551 | 1.500 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | fused_prologue_active_offset_gemm | 214.048 | 1.454 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | fused_prologue_active_offset_gemm | 238.827 | 1.508 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | fused_prologue_offset_gemm | 198.787 | 1.479 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 52 | fused_prologue_offset_gemm | 201.023 | 1.466 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | fused_prologue_offset_gemm | 206.915 | 1.499 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | fused_prologue_offset_gemm | 225.997 | 1.562 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- The fused SiLU+quant candidate is exact against the manual staged path for this route replay.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
