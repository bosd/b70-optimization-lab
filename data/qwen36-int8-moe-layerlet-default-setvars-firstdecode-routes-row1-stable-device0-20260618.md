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

- Mean `xpu_fused_moe`: `315.996 us`.
- Mean scratch `xpu_fused_moe`: `261.329 us`.
- Mean preallocated staged: `204.492 us`.
- Mean fused-prologue staged: `275.782 us`.
- Mean fused-prologue offset-GEMM staged: `202.102 us`.
- Mean fused-prologue active-offset-GEMM staged: `203.777 us`.
- Mean fused-prologue middle-layerlet staged: `173.267 us`.
- Mean full C++ layerlet: `169.172 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 304.607 | 254.660 | 202.965 | 273.107 | 202.055 | 196.895 | 167.575 | 164.791 | 91.976 | 92.401 | 170.654 |
| 1 | 5 | 8 | 302.501 | 250.682 | 194.844 | 264.841 | 194.981 | 195.832 | 166.012 | 161.124 | 92.277 | 91.501 | 162.538 |
| 1 | 10 | 8 | 304.840 | 253.091 | 199.763 | 266.474 | 194.504 | 195.244 | 167.957 | 163.909 | 93.200 | 92.007 | 163.887 |
| 1 | 15 | 8 | 294.490 | 247.478 | 190.984 | 258.218 | 189.543 | 192.194 | 163.933 | 158.326 | 91.083 | 91.641 | 160.134 |
| 1 | 20 | 8 | 296.948 | 244.920 | 191.629 | 259.062 | 187.493 | 189.571 | 161.226 | 159.195 | 90.608 | 90.116 | 159.049 |
| 1 | 25 | 8 | 303.777 | 251.495 | 195.790 | 264.103 | 194.088 | 196.550 | 167.733 | 161.216 | 92.548 | 92.409 | 162.705 |
| 1 | 30 | 8 | 297.528 | 245.277 | 190.062 | 257.748 | 187.850 | 189.422 | 161.250 | 158.815 | 90.359 | 90.794 | 159.808 |
| 1 | 35 | 8 | 296.506 | 246.459 | 192.667 | 258.695 | 187.379 | 189.157 | 162.559 | 159.491 | 90.043 | 90.158 | 159.557 |
| 1 | 40 | 8 | 296.712 | 246.061 | 193.728 | 259.154 | 188.682 | 190.847 | 163.684 | 162.656 | 90.707 | 93.290 | 161.670 |
| 1 | 45 | 8 | 293.876 | 249.246 | 192.527 | 256.987 | 187.916 | 192.013 | 164.495 | 159.553 | 90.842 | 91.331 | 159.357 |
| 1 | 50 | 8 | 309.981 | 257.286 | 199.905 | 271.937 | 200.543 | 201.913 | 169.948 | 166.599 | 93.555 | 93.784 | 163.946 |
| 1 | 55 | 8 | 301.867 | 247.863 | 194.327 | 264.826 | 191.644 | 192.960 | 166.169 | 163.956 | 93.002 | 92.995 | 164.114 |
| 1 | 60 | 8 | 297.603 | 249.141 | 192.570 | 258.986 | 191.058 | 192.923 | 163.670 | 160.819 | 93.000 | 91.560 | 162.413 |
| 1 | 65 | 8 | 300.453 | 246.929 | 192.324 | 261.506 | 192.100 | 194.340 | 164.641 | 161.758 | 93.278 | 93.271 | 164.783 |
| 1 | 70 | 8 | 311.490 | 256.610 | 200.997 | 273.092 | 200.221 | 202.301 | 173.574 | 168.686 | 97.313 | 96.977 | 170.808 |
| 1 | 75 | 8 | 324.345 | 267.233 | 209.151 | 282.384 | 210.678 | 210.669 | 181.142 | 174.566 | 100.705 | 100.369 | 177.759 |
| 1 | 80 | 8 | 349.825 | 287.458 | 241.694 | 299.421 | 222.908 | 223.224 | 193.359 | 188.257 | 104.863 | 103.827 | 181.515 |
| 1 | 85 | 8 | 393.881 | 321.391 | 242.540 | 339.220 | 246.906 | 249.137 | 206.948 | 205.267 | 115.527 | 116.898 | 199.928 |
| 1 | 90 | 8 | 317.836 | 262.746 | 205.275 | 276.579 | 200.058 | 202.020 | 169.777 | 165.608 | 97.271 | 96.729 | 170.638 |
| 1 | 95 | 8 | 376.480 | 307.549 | 237.411 | 323.417 | 237.912 | 243.726 | 206.034 | 197.813 | 112.993 | 112.594 | 193.880 |
| 1 | 100 | 8 | 339.387 | 279.181 | 220.768 | 300.468 | 215.940 | 219.929 | 186.396 | 182.699 | 103.913 | 105.862 | 185.262 |
| 1 | 105 | 8 | 323.967 | 263.510 | 206.171 | 282.100 | 207.884 | 208.806 | 175.711 | 170.444 | 95.976 | 95.590 | 168.620 |
| 1 | 110 | 8 | 317.306 | 262.843 | 206.596 | 278.878 | 206.085 | 207.464 | 174.318 | 170.719 | 95.363 | 94.713 | 172.247 |
| 1 | 115 | 8 | 327.706 | 272.799 | 213.122 | 287.563 | 212.009 | 213.521 | 180.296 | 173.860 | 100.693 | 98.025 | 173.202 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `5` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `158.326 us` (`1.860x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 164.791 | 1.848 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 161.124 | 1.877 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | full_layerlet | 163.909 | 1.860 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 158.326 | 1.860 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 20 | full_layerlet | 159.195 | 1.865 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 25 | full_layerlet | 161.216 | 1.884 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 30 | full_layerlet | 158.815 | 1.873 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 35 | full_layerlet | 159.491 | 1.859 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 40 | full_layerlet | 162.656 | 1.824 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 45 | full_layerlet | 159.553 | 1.842 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 50 | full_layerlet | 166.599 | 1.861 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 163.956 | 1.841 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 160.819 | 1.851 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 161.758 | 1.857 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 168.686 | 1.847 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 75 | full_layerlet | 174.566 | 1.858 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 188.257 | 1.858 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 205.267 | 1.919 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 165.608 | 1.919 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 197.813 | 1.903 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 182.699 | 1.858 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 105 | full_layerlet | 170.444 | 1.901 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 170.719 | 1.859 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 173.860 | 1.885 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
