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

- Mean `xpu_fused_moe`: `307.250 us`.
- Mean scratch `xpu_fused_moe`: `255.600 us`.
- Mean preallocated staged: `196.001 us`.
- Mean fused-prologue staged: `267.246 us`.
- Mean fused-prologue offset-GEMM staged: `196.699 us`.
- Mean fused-prologue active-offset-GEMM staged: `198.018 us`.
- Mean fused-prologue middle-layerlet staged: `168.399 us`.
- Mean full C++ layerlet: `163.868 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 298.795 | 248.148 | 191.908 | 262.278 | 200.259 | 196.660 | 167.068 | 162.611 | 94.542 | 100.991 | 169.113 |
| 1 | 5 | 8 | 300.870 | 248.313 | 191.639 | 259.564 | 191.325 | 192.892 | 164.871 | 161.009 | 96.755 | 94.311 | 166.917 |
| 1 | 10 | 8 | 339.137 | 274.649 | 212.448 | 293.865 | 225.226 | 223.266 | 189.026 | 181.838 | 103.014 | 102.420 | 181.401 |
| 1 | 15 | 8 | 298.543 | 251.283 | 192.759 | 262.750 | 194.000 | 193.479 | 164.316 | 158.760 | 92.566 | 94.989 | 162.003 |
| 1 | 20 | 8 | 297.219 | 252.521 | 192.075 | 259.804 | 190.170 | 193.455 | 164.142 | 159.455 | 92.701 | 92.372 | 165.325 |
| 1 | 25 | 8 | 307.995 | 259.333 | 197.314 | 270.238 | 201.903 | 199.137 | 168.495 | 163.401 | 94.918 | 95.125 | 166.687 |
| 1 | 30 | 8 | 296.413 | 250.323 | 191.087 | 258.458 | 189.818 | 188.601 | 161.108 | 157.031 | 92.352 | 92.910 | 165.252 |
| 1 | 35 | 8 | 296.333 | 248.649 | 191.411 | 263.043 | 190.253 | 191.927 | 163.451 | 158.533 | 92.198 | 91.682 | 161.731 |
| 1 | 40 | 8 | 320.325 | 266.139 | 202.220 | 274.618 | 201.384 | 205.932 | 174.168 | 175.859 | 98.752 | 97.519 | 175.766 |
| 1 | 45 | 8 | 315.123 | 265.443 | 200.819 | 274.075 | 199.012 | 201.549 | 173.042 | 167.029 | 97.983 | 98.653 | 173.155 |
| 1 | 50 | 8 | 309.929 | 255.878 | 195.840 | 267.741 | 196.943 | 202.588 | 170.024 | 162.977 | 99.755 | 96.524 | 169.939 |
| 1 | 55 | 8 | 343.764 | 292.887 | 223.422 | 297.804 | 218.554 | 219.205 | 184.977 | 180.505 | 104.024 | 103.128 | 181.523 |
| 1 | 60 | 8 | 374.870 | 307.457 | 232.239 | 326.540 | 237.783 | 240.113 | 206.948 | 203.502 | 113.851 | 111.385 | 203.814 |
| 1 | 65 | 8 | 315.698 | 261.113 | 200.790 | 277.595 | 201.342 | 206.019 | 172.248 | 167.627 | 97.785 | 98.562 | 171.281 |
| 1 | 70 | 8 | 291.905 | 241.885 | 187.705 | 254.278 | 186.113 | 186.809 | 160.826 | 155.547 | 91.309 | 90.410 | 159.346 |
| 1 | 75 | 8 | 301.658 | 250.865 | 191.729 | 261.377 | 192.175 | 193.472 | 164.212 | 158.158 | 92.743 | 92.873 | 168.226 |
| 1 | 80 | 8 | 300.101 | 250.042 | 192.269 | 260.988 | 191.849 | 192.502 | 163.123 | 161.104 | 93.250 | 93.538 | 164.657 |
| 1 | 85 | 8 | 300.781 | 249.887 | 192.207 | 261.703 | 192.167 | 194.453 | 165.005 | 160.061 | 92.745 | 92.991 | 164.026 |
| 1 | 90 | 8 | 303.786 | 251.880 | 192.293 | 261.139 | 191.630 | 194.122 | 164.835 | 159.936 | 92.958 | 92.566 | 162.917 |
| 1 | 95 | 8 | 293.787 | 244.446 | 189.141 | 254.651 | 186.970 | 189.313 | 162.733 | 156.613 | 90.826 | 91.670 | 160.564 |
| 1 | 100 | 8 | 286.033 | 237.552 | 183.484 | 250.340 | 183.279 | 184.300 | 156.550 | 154.045 | 89.684 | 88.625 | 155.436 |
| 1 | 105 | 8 | 288.793 | 239.160 | 185.198 | 251.054 | 184.526 | 186.253 | 158.995 | 154.149 | 90.760 | 89.741 | 156.828 |
| 1 | 110 | 8 | 291.085 | 238.625 | 183.498 | 250.156 | 183.920 | 185.231 | 157.719 | 154.859 | 90.005 | 89.948 | 157.979 |
| 1 | 115 | 8 | 301.050 | 247.922 | 190.538 | 259.849 | 190.184 | 191.144 | 163.691 | 158.210 | 92.465 | 91.988 | 161.877 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `12` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `154.045 us` (`1.857x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 162.611 | 1.837 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 161.009 | 1.869 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | full_layerlet | 181.838 | 1.865 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 158.760 | 1.880 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 20 | full_layerlet | 159.455 | 1.864 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 25 | full_layerlet | 163.401 | 1.885 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 30 | full_layerlet | 157.031 | 1.888 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 35 | full_layerlet | 158.533 | 1.869 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 40 | fused_prologue_middle_layerlet | 174.168 | 1.839 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 45 | full_layerlet | 167.029 | 1.887 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 162.977 | 1.902 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 180.505 | 1.904 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 203.502 | 1.842 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 167.627 | 1.883 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 155.547 | 1.877 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 75 | full_layerlet | 158.158 | 1.907 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 80 | full_layerlet | 161.104 | 1.863 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 160.061 | 1.879 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 159.936 | 1.899 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 95 | full_layerlet | 156.613 | 1.876 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 100 | full_layerlet | 154.045 | 1.857 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 105 | full_layerlet | 154.149 | 1.873 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 110 | full_layerlet | 154.859 | 1.880 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 115 | full_layerlet | 158.210 | 1.903 | True | candidate_layerlet_meets_speed_and_exactness_gate |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
