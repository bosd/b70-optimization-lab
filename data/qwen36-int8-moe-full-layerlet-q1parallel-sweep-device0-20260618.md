# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `16`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
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
- Fused-prologue middle-layerlet max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `340.875 us`.
- Mean scratch `xpu_fused_moe`: `279.222 us`.
- Mean preallocated staged: `216.419 us`.
- Mean fused-prologue staged: `295.691 us`.
- Mean fused-prologue offset-GEMM staged: `214.838 us`.
- Mean fused-prologue active-offset-GEMM staged: `216.393 us`.
- Mean fused-prologue middle-layerlet staged: `184.546 us`.
- Mean full C++ layerlet: `178.733 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 325.849 | 269.147 | 208.551 | 284.764 | 207.969 | 211.784 | 179.462 | 173.366 | 100.483 | 98.654 | 175.257 |
| 1 | 4 | 8 | 323.483 | 263.084 | 204.362 | 280.491 | 202.679 | 205.455 | 176.502 | 167.814 | 99.027 | 96.004 | 172.099 |
| 1 | 8 | 8 | 315.772 | 261.496 | 204.743 | 270.116 | 197.508 | 200.892 | 171.025 | 168.957 | 97.644 | 96.755 | 169.563 |
| 1 | 12 | 8 | 314.496 | 257.033 | 200.834 | 273.544 | 200.283 | 202.238 | 172.174 | 166.974 | 95.328 | 94.539 | 166.537 |
| 1 | 16 | 8 | 344.668 | 273.421 | 215.592 | 290.337 | 209.641 | 212.136 | 181.471 | 177.921 | 101.483 | 100.048 | 178.346 |
| 1 | 20 | 8 | 329.931 | 276.033 | 214.810 | 295.346 | 213.717 | 214.424 | 181.776 | 175.375 | 99.960 | 99.590 | 176.552 |
| 1 | 24 | 8 | 356.146 | 286.615 | 225.859 | 304.822 | 222.882 | 221.617 | 192.143 | 185.739 | 106.215 | 105.506 | 186.266 |
| 1 | 28 | 8 | 333.525 | 273.624 | 210.583 | 287.848 | 207.693 | 210.740 | 180.095 | 173.368 | 101.684 | 100.578 | 177.746 |
| 1 | 32 | 8 | 389.610 | 313.576 | 240.261 | 330.370 | 242.136 | 241.433 | 206.400 | 202.214 | 113.155 | 111.987 | 194.378 |
| 1 | 36 | 8 | 378.794 | 312.513 | 241.405 | 334.854 | 242.523 | 241.528 | 205.166 | 197.805 | 114.481 | 117.950 | 207.428 |
| 1 | 40 | 8 | 304.087 | 254.155 | 195.503 | 263.897 | 193.563 | 194.977 | 165.866 | 160.385 | 93.980 | 96.080 | 163.580 |
| 1 | 44 | 8 | 349.745 | 282.885 | 219.327 | 302.903 | 217.639 | 221.881 | 192.436 | 185.068 | 107.371 | 104.127 | 182.057 |
| 1 | 48 | 8 | 370.945 | 308.939 | 234.184 | 318.412 | 227.838 | 230.573 | 195.132 | 189.186 | 109.533 | 110.346 | 192.750 |
| 1 | 52 | 8 | 302.427 | 248.433 | 193.312 | 264.453 | 193.558 | 193.345 | 164.648 | 160.973 | 94.205 | 93.628 | 164.154 |
| 1 | 56 | 8 | 336.759 | 281.161 | 219.305 | 300.395 | 219.714 | 218.310 | 186.044 | 179.516 | 103.298 | 102.953 | 178.580 |
| 1 | 60 | 8 | 377.756 | 305.432 | 234.081 | 328.498 | 238.061 | 240.961 | 202.396 | 195.071 | 112.322 | 111.824 | 195.749 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `16`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `160.385 us` (`1.896x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 173.366 | 1.880 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | full_layerlet | 167.814 | 1.928 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | full_layerlet | 168.957 | 1.869 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | full_layerlet | 166.974 | 1.884 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | full_layerlet | 177.921 | 1.937 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 175.375 | 1.881 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | full_layerlet | 185.739 | 1.917 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | full_layerlet | 173.368 | 1.924 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | full_layerlet | 202.214 | 1.927 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | full_layerlet | 197.805 | 1.915 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 160.385 | 1.896 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | full_layerlet | 185.068 | 1.890 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | full_layerlet | 189.186 | 1.961 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 52 | full_layerlet | 160.973 | 1.879 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | full_layerlet | 179.516 | 1.876 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 195.071 | 1.937 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
