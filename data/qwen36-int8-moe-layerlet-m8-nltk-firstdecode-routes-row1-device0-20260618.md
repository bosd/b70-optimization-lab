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

- Mean `xpu_fused_moe`: `330.386 us`.
- Mean scratch `xpu_fused_moe`: `271.184 us`.
- Mean preallocated staged: `210.346 us`.
- Mean fused-prologue staged: `285.387 us`.
- Mean fused-prologue offset-GEMM staged: `207.747 us`.
- Mean fused-prologue active-offset-GEMM staged: `209.365 us`.
- Mean fused-prologue middle-layerlet staged: `179.167 us`.
- Mean full C++ layerlet: `175.271 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 300.516 | 249.880 | 194.276 | 261.115 | 194.120 | 191.101 | 162.323 | 161.125 | 94.642 | 96.269 | 168.259 |
| 1 | 5 | 8 | 305.679 | 249.917 | 194.344 | 262.592 | 192.170 | 192.648 | 168.033 | 165.533 | 94.069 | 93.472 | 164.736 |
| 1 | 10 | 8 | 378.484 | 297.370 | 233.660 | 319.443 | 234.111 | 235.800 | 207.036 | 193.371 | 113.588 | 111.203 | 200.649 |
| 1 | 15 | 8 | 361.161 | 299.338 | 232.623 | 316.226 | 231.500 | 231.439 | 197.316 | 190.312 | 110.110 | 111.569 | 195.412 |
| 1 | 20 | 8 | 389.087 | 319.052 | 248.394 | 325.752 | 245.818 | 249.434 | 206.314 | 202.766 | 118.132 | 117.057 | 202.811 |
| 1 | 25 | 8 | 287.007 | 241.417 | 186.714 | 252.580 | 183.712 | 186.450 | 161.639 | 157.630 | 89.273 | 90.165 | 158.109 |
| 1 | 30 | 8 | 322.743 | 265.707 | 206.375 | 281.675 | 203.379 | 202.846 | 178.495 | 175.333 | 98.892 | 99.820 | 173.882 |
| 1 | 35 | 8 | 295.309 | 241.830 | 189.271 | 256.814 | 184.424 | 185.783 | 159.201 | 156.016 | 90.896 | 91.314 | 159.076 |
| 1 | 40 | 8 | 316.799 | 257.163 | 199.222 | 267.528 | 192.946 | 197.870 | 170.259 | 167.205 | 96.116 | 95.200 | 168.559 |
| 1 | 45 | 8 | 323.123 | 268.948 | 208.950 | 281.614 | 205.198 | 203.205 | 173.366 | 169.365 | 99.436 | 99.885 | 174.182 |
| 1 | 50 | 8 | 344.420 | 275.905 | 212.819 | 284.606 | 211.712 | 211.833 | 180.766 | 177.547 | 100.880 | 101.641 | 175.030 |
| 1 | 55 | 8 | 354.729 | 286.500 | 223.514 | 302.788 | 218.517 | 229.121 | 190.943 | 186.583 | 106.684 | 108.880 | 184.399 |
| 1 | 60 | 8 | 310.512 | 256.148 | 197.622 | 269.601 | 193.804 | 196.917 | 167.283 | 165.118 | 96.741 | 94.828 | 165.174 |
| 1 | 65 | 8 | 300.446 | 249.925 | 193.076 | 262.465 | 189.314 | 190.130 | 164.818 | 160.852 | 94.080 | 94.444 | 163.826 |
| 1 | 70 | 8 | 286.163 | 238.363 | 184.944 | 251.165 | 181.358 | 182.955 | 158.418 | 155.290 | 89.865 | 90.411 | 157.722 |
| 1 | 75 | 8 | 335.337 | 277.903 | 217.950 | 292.950 | 212.826 | 216.906 | 183.996 | 179.934 | 101.854 | 106.788 | 180.833 |
| 1 | 80 | 8 | 313.049 | 258.502 | 199.507 | 273.073 | 199.389 | 198.762 | 171.542 | 170.957 | 96.941 | 97.158 | 171.193 |
| 1 | 85 | 8 | 335.896 | 277.118 | 212.979 | 288.778 | 209.700 | 208.837 | 178.663 | 175.302 | 102.406 | 103.095 | 180.688 |
| 1 | 90 | 8 | 376.425 | 310.787 | 237.826 | 333.762 | 242.349 | 244.849 | 204.260 | 201.587 | 113.472 | 115.172 | 198.984 |
| 1 | 95 | 8 | 354.170 | 291.712 | 226.227 | 319.340 | 227.031 | 233.691 | 197.809 | 191.510 | 108.967 | 108.842 | 187.990 |
| 1 | 100 | 8 | 316.111 | 258.743 | 198.387 | 269.123 | 194.929 | 196.323 | 167.182 | 164.512 | 97.530 | 95.522 | 167.450 |
| 1 | 105 | 8 | 325.325 | 269.335 | 208.339 | 280.460 | 203.136 | 204.498 | 179.083 | 173.229 | 98.917 | 98.450 | 170.752 |
| 1 | 110 | 8 | 373.818 | 300.106 | 232.139 | 311.547 | 228.083 | 229.280 | 196.587 | 192.108 | 109.688 | 108.536 | 192.156 |
| 1 | 115 | 8 | 322.950 | 266.757 | 209.146 | 284.286 | 206.413 | 204.082 | 174.675 | 173.325 | 99.085 | 100.224 | 176.983 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `3` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `155.290 us` (`1.843x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 161.125 | 1.865 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 165.533 | 1.847 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | full_layerlet | 193.371 | 1.957 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 190.312 | 1.898 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 202.766 | 1.919 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 25 | full_layerlet | 157.630 | 1.821 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 30 | full_layerlet | 175.333 | 1.841 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 35 | full_layerlet | 156.016 | 1.893 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 40 | full_layerlet | 167.205 | 1.895 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 45 | full_layerlet | 169.365 | 1.908 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 177.547 | 1.940 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 186.583 | 1.901 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 165.118 | 1.881 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 160.852 | 1.868 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 155.290 | 1.843 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 75 | full_layerlet | 179.934 | 1.864 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 170.957 | 1.831 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 175.302 | 1.916 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 201.587 | 1.867 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 191.510 | 1.849 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 164.512 | 1.922 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 105 | full_layerlet | 173.229 | 1.878 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 192.108 | 1.946 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 173.325 | 1.863 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
