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

- Mean `xpu_fused_moe`: `316.474 us`.
- Mean scratch `xpu_fused_moe`: `262.639 us`.
- Mean preallocated staged: `203.759 us`.
- Mean fused-prologue staged: `277.333 us`.
- Mean fused-prologue offset-GEMM staged: `203.241 us`.
- Mean fused-prologue active-offset-GEMM staged: `204.650 us`.
- Mean fused-prologue middle-layerlet staged: `173.428 us`.
- Mean full C++ layerlet: `169.210 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 330.581 | 275.888 | 216.164 | 287.919 | 233.532 | 212.040 | 179.523 | 177.705 | 103.719 | 103.104 | 178.513 |
| 1 | 5 | 8 | 311.617 | 257.830 | 198.987 | 268.084 | 193.457 | 197.472 | 166.863 | 164.585 | 93.442 | 93.525 | 165.968 |
| 1 | 10 | 8 | 308.681 | 262.420 | 202.386 | 287.303 | 199.458 | 201.542 | 169.908 | 165.632 | 94.250 | 94.347 | 166.669 |
| 1 | 15 | 8 | 312.106 | 260.265 | 201.736 | 273.647 | 200.079 | 202.623 | 171.071 | 165.838 | 94.534 | 94.321 | 168.648 |
| 1 | 20 | 8 | 341.233 | 283.383 | 221.797 | 305.441 | 216.187 | 216.126 | 190.526 | 187.165 | 99.809 | 102.672 | 180.866 |
| 1 | 25 | 8 | 309.138 | 256.941 | 199.800 | 272.173 | 200.765 | 204.124 | 171.291 | 164.055 | 94.954 | 93.662 | 167.584 |
| 1 | 30 | 8 | 313.078 | 259.893 | 201.628 | 273.622 | 202.034 | 203.206 | 171.936 | 167.237 | 95.085 | 94.675 | 166.904 |
| 1 | 35 | 8 | 310.352 | 258.976 | 200.720 | 271.755 | 199.940 | 202.933 | 170.990 | 165.719 | 93.931 | 94.370 | 167.216 |
| 1 | 40 | 8 | 331.514 | 276.879 | 215.325 | 292.055 | 212.507 | 213.964 | 182.558 | 177.622 | 99.528 | 101.273 | 178.376 |
| 1 | 45 | 8 | 297.849 | 250.562 | 193.494 | 260.563 | 190.209 | 192.688 | 164.029 | 159.604 | 91.565 | 90.976 | 161.224 |
| 1 | 50 | 8 | 293.417 | 248.525 | 188.906 | 255.840 | 189.216 | 189.769 | 161.001 | 157.215 | 91.492 | 89.922 | 158.723 |
| 1 | 55 | 8 | 333.930 | 268.471 | 207.879 | 284.185 | 207.477 | 209.957 | 176.753 | 171.988 | 97.677 | 97.006 | 172.434 |
| 1 | 60 | 8 | 328.418 | 265.859 | 207.040 | 280.153 | 202.771 | 211.477 | 176.947 | 175.448 | 98.209 | 98.446 | 176.651 |
| 1 | 65 | 8 | 307.211 | 254.313 | 198.104 | 273.165 | 197.992 | 200.467 | 169.629 | 166.925 | 92.066 | 92.791 | 162.984 |
| 1 | 70 | 8 | 330.458 | 273.139 | 211.378 | 286.309 | 209.238 | 213.597 | 180.944 | 174.015 | 99.393 | 99.791 | 175.096 |
| 1 | 75 | 8 | 312.926 | 257.528 | 200.401 | 271.203 | 198.827 | 203.131 | 171.728 | 168.145 | 94.335 | 94.401 | 167.208 |
| 1 | 80 | 8 | 312.251 | 257.956 | 200.666 | 276.959 | 198.884 | 201.022 | 170.387 | 168.275 | 94.945 | 93.829 | 166.882 |
| 1 | 85 | 8 | 309.483 | 257.447 | 200.651 | 272.043 | 201.191 | 202.760 | 172.463 | 167.478 | 94.073 | 93.723 | 166.979 |
| 1 | 90 | 8 | 309.792 | 256.847 | 200.368 | 273.522 | 200.964 | 203.187 | 169.898 | 165.384 | 93.876 | 94.030 | 167.014 |
| 1 | 95 | 8 | 354.895 | 292.490 | 226.072 | 305.692 | 227.992 | 226.699 | 193.764 | 188.859 | 106.513 | 104.926 | 188.689 |
| 1 | 100 | 8 | 310.527 | 257.168 | 199.550 | 271.596 | 199.836 | 201.424 | 169.175 | 165.696 | 93.619 | 94.569 | 164.930 |
| 1 | 105 | 8 | 309.336 | 257.989 | 199.167 | 272.267 | 199.120 | 200.541 | 169.419 | 166.164 | 94.751 | 93.350 | 165.641 |
| 1 | 110 | 8 | 308.532 | 256.892 | 199.982 | 270.863 | 199.243 | 201.379 | 169.927 | 165.417 | 93.919 | 94.082 | 166.547 |
| 1 | 115 | 8 | 308.055 | 255.675 | 198.019 | 269.627 | 196.877 | 199.482 | 171.536 | 164.856 | 93.737 | 92.822 | 165.041 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `2` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `157.215 us` (`1.866x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 177.705 | 1.860 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 164.585 | 1.893 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | full_layerlet | 165.632 | 1.864 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 165.838 | 1.882 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 187.165 | 1.823 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 25 | full_layerlet | 164.055 | 1.884 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 30 | full_layerlet | 167.237 | 1.872 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 35 | full_layerlet | 165.719 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 177.622 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 45 | full_layerlet | 159.604 | 1.866 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 50 | full_layerlet | 157.215 | 1.866 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 55 | full_layerlet | 171.988 | 1.942 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 175.448 | 1.872 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 166.925 | 1.840 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 174.015 | 1.899 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 75 | full_layerlet | 168.145 | 1.861 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 168.275 | 1.856 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 167.478 | 1.848 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 165.384 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 188.859 | 1.879 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 165.696 | 1.874 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 105 | full_layerlet | 166.164 | 1.862 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 165.417 | 1.865 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 164.856 | 1.869 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
