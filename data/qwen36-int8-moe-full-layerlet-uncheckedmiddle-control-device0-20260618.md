# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- Full layerlet unchecked-middle enabled: `False`.
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

- Mean `xpu_fused_moe`: `324.762 us`.
- Mean scratch `xpu_fused_moe`: `268.050 us`.
- Mean preallocated staged: `208.663 us`.
- Mean fused-prologue staged: `283.131 us`.
- Mean fused-prologue offset-GEMM staged: `206.520 us`.
- Mean fused-prologue active-offset-GEMM staged: `209.011 us`.
- Mean fused-prologue middle-layerlet staged: `177.802 us`.
- Mean full C++ layerlet: `171.858 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 318.413 | 256.010 | 200.666 | 273.686 | 199.058 | 202.895 | 171.493 | 166.008 | 96.483 | 95.309 | 167.215 |
| 1 | 4 | 8 | 321.050 | 261.707 | 205.535 | 284.343 | 202.594 | 204.589 | 172.049 | 167.603 | 96.602 | 96.351 | 169.496 |
| 1 | 8 | 8 | 360.060 | 294.244 | 231.679 | 313.118 | 229.885 | 227.893 | 193.308 | 191.336 | 105.588 | 108.498 | 187.047 |
| 1 | 12 | 8 | 314.376 | 263.536 | 205.345 | 278.587 | 203.147 | 200.841 | 172.078 | 166.754 | 95.025 | 94.078 | 167.001 |
| 1 | 16 | 8 | 358.136 | 297.877 | 226.517 | 310.079 | 223.905 | 233.861 | 199.774 | 187.928 | 109.749 | 111.010 | 195.981 |
| 1 | 20 | 8 | 318.131 | 257.209 | 201.306 | 271.242 | 200.684 | 200.869 | 172.987 | 171.146 | 96.737 | 94.389 | 167.650 |
| 1 | 24 | 8 | 350.811 | 289.981 | 224.345 | 310.573 | 229.174 | 231.475 | 197.902 | 184.623 | 108.205 | 106.226 | 186.975 |
| 1 | 28 | 8 | 329.604 | 270.549 | 210.527 | 284.653 | 205.369 | 208.560 | 183.773 | 172.959 | 98.854 | 98.852 | 172.997 |
| 1 | 32 | 8 | 293.433 | 244.871 | 191.656 | 256.823 | 187.067 | 189.927 | 162.458 | 157.361 | 89.979 | 89.459 | 159.035 |
| 1 | 36 | 8 | 302.338 | 250.782 | 196.406 | 263.279 | 192.254 | 195.532 | 166.154 | 159.013 | 91.194 | 92.179 | 161.892 |
| 1 | 40 | 8 | 302.768 | 246.806 | 194.449 | 263.765 | 190.644 | 192.669 | 163.606 | 160.560 | 92.298 | 91.340 | 161.351 |
| 1 | 44 | 8 | 326.130 | 274.475 | 212.352 | 286.338 | 208.350 | 211.999 | 179.814 | 176.609 | 99.590 | 99.289 | 174.441 |
| 1 | 48 | 8 | 340.160 | 279.965 | 220.284 | 295.812 | 217.133 | 219.825 | 185.420 | 179.138 | 100.972 | 104.629 | 177.556 |
| 1 | 52 | 8 | 309.757 | 255.464 | 198.217 | 267.131 | 196.056 | 199.058 | 168.154 | 163.771 | 94.359 | 94.139 | 163.805 |
| 1 | 56 | 8 | 327.411 | 276.505 | 211.531 | 288.716 | 211.040 | 214.025 | 179.554 | 174.160 | 99.041 | 97.954 | 173.928 |
| 1 | 60 | 8 | 323.612 | 268.814 | 207.797 | 281.949 | 207.964 | 210.151 | 176.311 | 170.768 | 96.928 | 96.562 | 171.033 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `2` / `16`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `157.361 us` (`1.865x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 166.008 | 1.918 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | full_layerlet | 167.603 | 1.916 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | full_layerlet | 191.336 | 1.882 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | full_layerlet | 166.754 | 1.885 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | full_layerlet | 187.928 | 1.906 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 171.146 | 1.859 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | full_layerlet | 184.623 | 1.900 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | full_layerlet | 172.959 | 1.906 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | full_layerlet | 157.361 | 1.865 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 36 | full_layerlet | 159.013 | 1.901 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 40 | full_layerlet | 160.560 | 1.886 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | full_layerlet | 176.609 | 1.847 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | full_layerlet | 179.138 | 1.899 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 52 | full_layerlet | 163.771 | 1.891 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | full_layerlet | 174.160 | 1.880 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 170.768 | 1.895 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
