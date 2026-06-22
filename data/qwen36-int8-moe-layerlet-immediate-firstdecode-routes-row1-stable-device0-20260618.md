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

- Mean `xpu_fused_moe`: `316.593 us`.
- Mean scratch `xpu_fused_moe`: `264.085 us`.
- Mean preallocated staged: `205.533 us`.
- Mean fused-prologue staged: `277.343 us`.
- Mean fused-prologue offset-GEMM staged: `203.069 us`.
- Mean fused-prologue active-offset-GEMM staged: `204.119 us`.
- Mean fused-prologue middle-layerlet staged: `173.664 us`.
- Mean full C++ layerlet: `169.618 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 321.346 | 272.223 | 211.373 | 284.135 | 215.727 | 211.221 | 178.622 | 178.733 | 98.342 | 100.944 | 177.091 |
| 1 | 5 | 8 | 317.216 | 265.826 | 206.015 | 277.784 | 205.201 | 204.084 | 172.987 | 168.964 | 95.458 | 95.129 | 168.977 |
| 1 | 10 | 8 | 349.480 | 286.877 | 236.988 | 299.851 | 217.256 | 218.988 | 188.419 | 183.281 | 102.764 | 104.409 | 182.627 |
| 1 | 15 | 8 | 303.694 | 256.861 | 197.985 | 268.578 | 195.111 | 197.200 | 169.326 | 162.505 | 94.155 | 92.584 | 163.082 |
| 1 | 20 | 8 | 324.062 | 271.854 | 210.915 | 284.471 | 211.390 | 215.039 | 182.529 | 173.583 | 98.211 | 99.296 | 177.386 |
| 1 | 25 | 8 | 300.286 | 251.479 | 194.555 | 267.008 | 194.038 | 195.541 | 165.540 | 160.848 | 92.340 | 91.244 | 167.197 |
| 1 | 30 | 8 | 323.761 | 272.317 | 209.765 | 281.566 | 207.579 | 209.004 | 177.046 | 171.749 | 96.597 | 99.765 | 171.127 |
| 1 | 35 | 8 | 329.250 | 272.154 | 211.699 | 288.212 | 209.695 | 210.773 | 179.752 | 173.883 | 98.821 | 98.876 | 171.671 |
| 1 | 40 | 8 | 316.552 | 262.886 | 204.518 | 279.056 | 208.518 | 205.842 | 174.491 | 170.056 | 95.895 | 95.467 | 168.007 |
| 1 | 45 | 8 | 318.131 | 262.780 | 204.731 | 280.093 | 206.010 | 206.573 | 174.470 | 171.572 | 94.839 | 94.519 | 167.277 |
| 1 | 50 | 8 | 306.318 | 253.065 | 198.669 | 267.621 | 193.421 | 195.234 | 167.192 | 165.436 | 93.153 | 93.004 | 165.251 |
| 1 | 55 | 8 | 292.401 | 246.275 | 191.381 | 258.428 | 186.720 | 188.876 | 162.027 | 158.643 | 89.927 | 89.702 | 157.447 |
| 1 | 60 | 8 | 293.972 | 246.000 | 190.022 | 257.582 | 187.138 | 190.214 | 162.063 | 157.265 | 89.482 | 90.040 | 161.323 |
| 1 | 65 | 8 | 306.056 | 253.592 | 197.108 | 266.895 | 193.835 | 194.671 | 165.674 | 164.252 | 93.506 | 93.311 | 163.623 |
| 1 | 70 | 8 | 300.373 | 249.510 | 195.076 | 261.425 | 191.682 | 191.646 | 165.691 | 163.833 | 91.681 | 91.993 | 160.983 |
| 1 | 75 | 8 | 326.898 | 272.563 | 210.285 | 280.947 | 208.496 | 211.104 | 180.194 | 175.403 | 98.403 | 99.240 | 175.280 |
| 1 | 80 | 8 | 327.954 | 272.832 | 213.160 | 292.228 | 208.461 | 209.557 | 181.081 | 177.346 | 99.114 | 101.915 | 175.249 |
| 1 | 85 | 8 | 345.030 | 286.560 | 223.513 | 298.679 | 219.047 | 217.190 | 185.160 | 183.142 | 101.755 | 104.445 | 180.430 |
| 1 | 90 | 8 | 351.428 | 292.795 | 226.065 | 305.068 | 224.363 | 226.982 | 190.447 | 188.032 | 105.480 | 106.042 | 187.327 |
| 1 | 95 | 8 | 324.288 | 274.212 | 212.399 | 288.241 | 208.822 | 211.191 | 178.795 | 173.151 | 97.566 | 97.146 | 172.056 |
| 1 | 100 | 8 | 310.934 | 260.603 | 202.427 | 272.530 | 202.687 | 201.961 | 169.697 | 164.131 | 93.049 | 92.832 | 164.415 |
| 1 | 105 | 8 | 305.042 | 249.442 | 194.418 | 265.971 | 192.712 | 195.215 | 166.819 | 162.079 | 92.272 | 91.964 | 162.029 |
| 1 | 110 | 8 | 292.540 | 250.881 | 192.169 | 259.773 | 191.705 | 194.437 | 163.696 | 160.080 | 91.874 | 91.161 | 157.184 |
| 1 | 115 | 8 | 311.222 | 254.459 | 197.564 | 270.086 | 194.045 | 196.326 | 166.221 | 162.854 | 93.990 | 93.922 | 167.178 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `2` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `157.265 us` (`1.869x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_middle_layerlet | 178.622 | 1.799 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 168.964 | 1.877 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | full_layerlet | 183.281 | 1.907 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 162.505 | 1.869 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 173.583 | 1.867 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 25 | full_layerlet | 160.848 | 1.867 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 30 | full_layerlet | 171.749 | 1.885 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 35 | full_layerlet | 173.883 | 1.894 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 170.056 | 1.861 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 45 | full_layerlet | 171.572 | 1.854 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 165.436 | 1.852 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 158.643 | 1.843 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 60 | full_layerlet | 157.265 | 1.869 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 65 | full_layerlet | 164.252 | 1.863 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 163.833 | 1.833 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 75 | full_layerlet | 175.403 | 1.864 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 177.346 | 1.849 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 183.142 | 1.884 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 188.032 | 1.869 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 173.151 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 164.131 | 1.894 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 105 | full_layerlet | 162.079 | 1.882 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 160.080 | 1.827 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 162.854 | 1.911 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
