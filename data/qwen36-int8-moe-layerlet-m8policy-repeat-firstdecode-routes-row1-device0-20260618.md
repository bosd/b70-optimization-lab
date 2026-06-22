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

- Mean `xpu_fused_moe`: `320.449 us`.
- Mean scratch `xpu_fused_moe`: `264.269 us`.
- Mean preallocated staged: `205.591 us`.
- Mean fused-prologue staged: `278.666 us`.
- Mean fused-prologue offset-GEMM staged: `204.530 us`.
- Mean fused-prologue active-offset-GEMM staged: `206.100 us`.
- Mean fused-prologue middle-layerlet staged: `175.815 us`.
- Mean full C++ layerlet: `170.817 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 351.035 | 284.215 | 218.655 | 303.573 | 233.693 | 222.958 | 186.816 | 184.102 | 109.332 | 104.887 | 188.189 |
| 1 | 5 | 8 | 288.710 | 244.071 | 190.832 | 256.719 | 189.953 | 192.326 | 163.766 | 158.986 | 90.688 | 94.828 | 159.174 |
| 1 | 10 | 8 | 337.326 | 274.642 | 214.688 | 293.625 | 216.800 | 216.550 | 184.167 | 178.564 | 105.512 | 103.446 | 179.814 |
| 1 | 15 | 8 | 311.654 | 258.635 | 200.174 | 275.318 | 201.847 | 200.476 | 173.677 | 167.806 | 96.568 | 96.109 | 170.189 |
| 1 | 20 | 8 | 322.163 | 263.531 | 207.224 | 281.684 | 206.628 | 207.712 | 175.432 | 171.491 | 98.271 | 98.236 | 173.259 |
| 1 | 25 | 8 | 321.608 | 272.431 | 205.734 | 278.462 | 203.530 | 208.630 | 178.965 | 171.314 | 99.141 | 97.243 | 170.194 |
| 1 | 30 | 8 | 285.932 | 238.983 | 185.656 | 250.875 | 182.535 | 184.196 | 159.003 | 154.458 | 89.248 | 89.599 | 157.366 |
| 1 | 35 | 8 | 347.858 | 276.069 | 215.757 | 294.198 | 216.160 | 222.019 | 187.656 | 184.684 | 103.700 | 102.696 | 181.681 |
| 1 | 40 | 8 | 306.545 | 255.052 | 204.639 | 269.780 | 194.588 | 197.644 | 169.490 | 165.639 | 93.629 | 94.589 | 166.863 |
| 1 | 45 | 8 | 341.623 | 280.904 | 217.056 | 294.910 | 216.066 | 218.042 | 183.896 | 178.517 | 102.188 | 102.149 | 185.988 |
| 1 | 50 | 8 | 332.450 | 268.864 | 208.250 | 282.537 | 209.229 | 210.564 | 179.196 | 174.101 | 101.179 | 100.741 | 178.754 |
| 1 | 55 | 8 | 309.078 | 254.818 | 199.781 | 267.886 | 196.901 | 197.142 | 168.686 | 163.689 | 94.648 | 94.274 | 165.743 |
| 1 | 60 | 8 | 308.472 | 254.830 | 198.217 | 267.465 | 196.019 | 198.927 | 169.080 | 163.165 | 94.892 | 93.977 | 168.529 |
| 1 | 65 | 8 | 305.437 | 254.873 | 196.800 | 266.835 | 196.129 | 197.632 | 167.503 | 162.788 | 93.781 | 94.358 | 165.653 |
| 1 | 70 | 8 | 305.858 | 254.210 | 197.802 | 265.991 | 195.590 | 198.530 | 168.030 | 161.623 | 94.191 | 93.517 | 166.469 |
| 1 | 75 | 8 | 327.380 | 269.646 | 208.538 | 287.464 | 209.982 | 209.903 | 178.491 | 172.962 | 100.026 | 100.873 | 177.597 |
| 1 | 80 | 8 | 315.148 | 261.396 | 203.273 | 275.590 | 199.115 | 203.911 | 177.118 | 173.958 | 100.595 | 97.970 | 170.444 |
| 1 | 85 | 8 | 326.500 | 263.399 | 207.358 | 277.521 | 202.257 | 204.781 | 174.108 | 167.302 | 98.856 | 97.497 | 173.273 |
| 1 | 90 | 8 | 329.897 | 271.366 | 212.413 | 285.951 | 210.868 | 212.436 | 180.714 | 174.974 | 100.420 | 101.571 | 178.684 |
| 1 | 95 | 8 | 314.979 | 262.943 | 203.797 | 276.667 | 201.993 | 202.427 | 177.793 | 169.451 | 97.575 | 96.667 | 172.905 |
| 1 | 100 | 8 | 319.512 | 269.219 | 209.137 | 284.307 | 205.241 | 206.238 | 176.384 | 174.212 | 98.561 | 99.488 | 176.663 |
| 1 | 105 | 8 | 363.908 | 298.967 | 230.156 | 311.981 | 230.330 | 232.313 | 197.943 | 195.076 | 111.097 | 110.471 | 195.681 |
| 1 | 110 | 8 | 301.912 | 251.413 | 194.990 | 262.378 | 191.080 | 194.332 | 167.076 | 161.165 | 93.967 | 93.432 | 164.691 |
| 1 | 115 | 8 | 315.790 | 257.986 | 203.257 | 276.269 | 202.193 | 206.708 | 174.562 | 169.580 | 99.158 | 96.708 | 171.479 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `2` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `154.458 us` (`1.851x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 184.102 | 1.907 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 158.986 | 1.816 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 10 | full_layerlet | 178.564 | 1.889 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 167.806 | 1.857 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 171.491 | 1.879 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 25 | full_layerlet | 171.314 | 1.877 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 30 | full_layerlet | 154.458 | 1.851 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 35 | full_layerlet | 184.684 | 1.884 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 165.639 | 1.851 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 45 | full_layerlet | 178.517 | 1.914 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 174.101 | 1.910 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 163.689 | 1.888 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 163.165 | 1.891 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 162.788 | 1.876 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 161.623 | 1.892 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 75 | full_layerlet | 172.962 | 1.893 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 173.958 | 1.812 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 167.302 | 1.952 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 174.974 | 1.885 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 169.451 | 1.859 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 174.212 | 1.834 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 105 | full_layerlet | 195.076 | 1.865 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 161.165 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 169.580 | 1.862 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
