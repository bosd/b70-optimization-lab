# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `24`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-firstdecode-route-fixture-routes-20260612ct.jsonl`.
- Route records matched: `120`; top-k rows loaded: `120`.
- Route start indices: `0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115`.
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

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `320.679 us`.
- Mean scratch `xpu_fused_moe`: `263.256 us`.
- Mean preallocated staged: `203.778 us`.
- Mean fused-prologue staged: `276.948 us`.
- Mean fused-prologue offset-GEMM staged: `202.195 us`.
- Mean fused-prologue active-offset-GEMM staged: `205.197 us`.
- Mean fused-prologue middle-layerlet staged: `174.214 us`.
- Mean full C++ layerlet: `170.198 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 316.794 | 261.518 | 200.744 | 277.954 | 205.020 | 202.089 | 170.858 | 171.688 | 96.585 | 100.833 | 172.638 |
| 1 | 5 | 8 | 366.539 | 293.980 | 225.826 | 305.330 | 219.943 | 232.738 | 189.729 | 195.201 | 107.822 | 105.827 | 187.769 |
| 1 | 10 | 8 | 318.772 | 263.266 | 203.616 | 275.551 | 203.251 | 203.403 | 174.801 | 169.811 | 97.249 | 95.467 | 167.069 |
| 1 | 15 | 8 | 324.319 | 261.541 | 201.571 | 274.763 | 204.656 | 203.757 | 175.259 | 169.402 | 98.207 | 96.153 | 171.347 |
| 1 | 20 | 8 | 308.064 | 252.840 | 197.394 | 266.420 | 193.742 | 197.160 | 167.142 | 166.017 | 93.311 | 92.943 | 165.159 |
| 1 | 25 | 8 | 306.829 | 253.339 | 196.966 | 266.675 | 195.510 | 196.184 | 167.045 | 161.604 | 92.900 | 96.599 | 165.492 |
| 1 | 30 | 8 | 292.543 | 240.599 | 187.602 | 253.992 | 183.784 | 185.907 | 158.624 | 156.156 | 89.674 | 89.551 | 157.884 |
| 1 | 35 | 8 | 291.772 | 241.894 | 187.039 | 254.013 | 184.297 | 187.065 | 159.515 | 156.054 | 89.073 | 90.111 | 157.203 |
| 1 | 40 | 8 | 299.260 | 247.075 | 191.691 | 260.806 | 189.185 | 192.771 | 163.616 | 161.335 | 91.213 | 91.151 | 159.916 |
| 1 | 45 | 8 | 331.171 | 279.061 | 209.903 | 285.974 | 211.205 | 210.529 | 182.281 | 175.084 | 100.478 | 101.036 | 179.939 |
| 1 | 50 | 8 | 321.086 | 272.620 | 207.461 | 275.792 | 202.615 | 207.113 | 172.798 | 168.896 | 97.883 | 97.788 | 173.051 |
| 1 | 55 | 8 | 313.127 | 260.055 | 199.704 | 270.332 | 197.907 | 201.387 | 171.472 | 164.566 | 94.952 | 94.333 | 167.397 |
| 1 | 60 | 8 | 299.087 | 246.743 | 191.201 | 260.569 | 189.583 | 192.897 | 163.953 | 159.931 | 90.782 | 90.653 | 161.177 |
| 1 | 65 | 8 | 310.244 | 250.039 | 194.371 | 269.207 | 197.061 | 199.028 | 167.832 | 163.693 | 93.375 | 94.274 | 164.925 |
| 1 | 70 | 8 | 310.686 | 255.542 | 198.075 | 275.083 | 200.810 | 201.413 | 172.642 | 164.490 | 93.999 | 94.285 | 164.426 |
| 1 | 75 | 8 | 356.751 | 285.887 | 228.935 | 307.306 | 220.369 | 226.295 | 192.714 | 186.018 | 110.607 | 104.830 | 187.628 |
| 1 | 80 | 8 | 380.465 | 307.003 | 242.284 | 326.882 | 237.961 | 249.031 | 210.253 | 207.490 | 113.877 | 113.828 | 199.209 |
| 1 | 85 | 8 | 328.238 | 268.110 | 207.686 | 279.233 | 203.493 | 206.456 | 176.916 | 172.957 | 98.408 | 97.906 | 171.936 |
| 1 | 90 | 8 | 321.577 | 267.587 | 206.452 | 278.188 | 204.223 | 206.048 | 175.443 | 170.243 | 97.717 | 96.957 | 170.435 |
| 1 | 95 | 8 | 309.717 | 253.098 | 196.487 | 266.455 | 194.972 | 196.529 | 168.485 | 163.902 | 93.652 | 96.583 | 164.067 |
| 1 | 100 | 8 | 330.775 | 269.906 | 208.367 | 289.240 | 207.334 | 214.283 | 180.866 | 175.876 | 100.487 | 98.143 | 174.668 |
| 1 | 105 | 8 | 329.846 | 273.232 | 210.103 | 285.451 | 209.926 | 210.709 | 177.753 | 173.952 | 101.610 | 99.365 | 177.325 |
| 1 | 110 | 8 | 319.902 | 258.161 | 199.574 | 270.960 | 198.772 | 201.675 | 171.210 | 165.327 | 95.664 | 94.590 | 167.776 |
| 1 | 115 | 8 | 308.729 | 255.044 | 197.628 | 270.582 | 197.052 | 200.254 | 169.920 | 165.050 | 93.005 | 92.974 | 164.720 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `3` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `156.054 us` (`1.870x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_middle_layerlet | 170.858 | 1.854 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | fused_prologue_middle_layerlet | 189.729 | 1.932 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | full_layerlet | 169.811 | 1.877 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 169.402 | 1.914 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 166.017 | 1.856 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 25 | full_layerlet | 161.604 | 1.899 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 30 | full_layerlet | 156.156 | 1.873 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 35 | full_layerlet | 156.054 | 1.870 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 40 | full_layerlet | 161.335 | 1.855 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 45 | full_layerlet | 175.084 | 1.891 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 168.896 | 1.901 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 164.566 | 1.903 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 159.931 | 1.870 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 65 | full_layerlet | 163.693 | 1.895 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 164.490 | 1.889 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 75 | full_layerlet | 186.018 | 1.918 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 207.490 | 1.834 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 172.957 | 1.898 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 170.243 | 1.889 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 163.902 | 1.890 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 175.876 | 1.881 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 105 | full_layerlet | 173.952 | 1.896 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 165.327 | 1.935 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 165.050 | 1.871 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
