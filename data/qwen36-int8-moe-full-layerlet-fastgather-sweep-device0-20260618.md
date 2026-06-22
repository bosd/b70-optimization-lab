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

- Mean `xpu_fused_moe`: `306.467 us`.
- Mean scratch `xpu_fused_moe`: `254.070 us`.
- Mean preallocated staged: `197.222 us`.
- Mean fused-prologue staged: `266.473 us`.
- Mean fused-prologue offset-GEMM staged: `194.838 us`.
- Mean fused-prologue active-offset-GEMM staged: `196.722 us`.
- Mean fused-prologue middle-layerlet staged: `166.919 us`.
- Mean full C++ layerlet: `161.622 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 321.530 | 267.152 | 207.492 | 285.208 | 206.806 | 208.151 | 176.285 | 168.579 | 98.526 | 98.462 | 171.699 |
| 1 | 4 | 8 | 327.484 | 270.395 | 211.775 | 279.103 | 202.417 | 208.185 | 174.997 | 170.463 | 99.147 | 98.174 | 171.253 |
| 1 | 8 | 8 | 308.166 | 257.457 | 199.252 | 266.828 | 194.988 | 196.617 | 167.203 | 161.845 | 93.792 | 93.850 | 172.683 |
| 1 | 12 | 8 | 310.234 | 261.225 | 201.668 | 271.235 | 199.493 | 201.263 | 169.667 | 165.355 | 94.013 | 94.274 | 166.213 |
| 1 | 16 | 8 | 309.546 | 255.788 | 197.961 | 269.804 | 196.359 | 197.976 | 169.270 | 163.540 | 94.871 | 95.399 | 166.877 |
| 1 | 20 | 8 | 306.389 | 256.426 | 196.095 | 266.900 | 196.446 | 197.560 | 167.705 | 161.448 | 94.650 | 94.425 | 164.975 |
| 1 | 24 | 8 | 296.185 | 247.302 | 191.487 | 259.497 | 188.571 | 191.091 | 162.545 | 157.799 | 91.414 | 91.413 | 167.690 |
| 1 | 28 | 8 | 311.083 | 255.597 | 198.683 | 269.100 | 197.257 | 198.895 | 168.067 | 162.497 | 94.619 | 93.921 | 166.651 |
| 1 | 32 | 8 | 307.519 | 253.356 | 195.669 | 266.933 | 194.438 | 196.810 | 165.984 | 161.847 | 94.687 | 93.276 | 165.233 |
| 1 | 36 | 8 | 295.925 | 246.735 | 192.327 | 257.308 | 188.900 | 190.871 | 163.906 | 158.054 | 90.853 | 91.362 | 161.136 |
| 1 | 40 | 8 | 308.088 | 254.847 | 197.512 | 267.635 | 196.293 | 197.806 | 167.480 | 161.748 | 94.122 | 96.890 | 166.424 |
| 1 | 44 | 8 | 305.178 | 251.592 | 194.742 | 263.685 | 193.766 | 193.759 | 165.343 | 161.165 | 93.207 | 93.205 | 164.114 |
| 1 | 48 | 8 | 292.888 | 241.214 | 189.776 | 255.384 | 187.385 | 186.252 | 158.662 | 155.116 | 89.924 | 89.584 | 158.437 |
| 1 | 52 | 8 | 293.689 | 243.308 | 192.643 | 258.242 | 187.138 | 188.113 | 160.224 | 156.381 | 90.821 | 90.334 | 159.042 |
| 1 | 56 | 8 | 302.626 | 247.626 | 192.046 | 261.054 | 191.719 | 196.505 | 163.738 | 158.538 | 91.693 | 92.078 | 161.805 |
| 1 | 60 | 8 | 306.944 | 255.098 | 196.428 | 265.658 | 195.428 | 197.695 | 169.627 | 161.576 | 94.791 | 94.096 | 166.887 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `5` / `16`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `155.116 us` (`1.888x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 168.579 | 1.907 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | full_layerlet | 170.463 | 1.921 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | full_layerlet | 161.845 | 1.904 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | full_layerlet | 165.355 | 1.876 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | full_layerlet | 163.540 | 1.893 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 161.448 | 1.898 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | full_layerlet | 157.799 | 1.877 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 28 | full_layerlet | 162.497 | 1.914 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | full_layerlet | 161.847 | 1.900 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | full_layerlet | 158.054 | 1.872 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 40 | full_layerlet | 161.748 | 1.905 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | full_layerlet | 161.165 | 1.894 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | full_layerlet | 155.116 | 1.888 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 52 | full_layerlet | 156.381 | 1.878 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 56 | full_layerlet | 158.538 | 1.909 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 60 | full_layerlet | 161.576 | 1.900 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
