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

- Mean `xpu_fused_moe`: `305.657 us`.
- Mean scratch `xpu_fused_moe`: `253.638 us`.
- Mean preallocated staged: `197.332 us`.
- Mean fused-prologue staged: `265.752 us`.
- Mean fused-prologue offset-GEMM staged: `196.384 us`.
- Mean fused-prologue active-offset-GEMM staged: `197.638 us`.
- Mean fused-prologue middle-layerlet staged: `168.174 us`.
- Mean full C++ layerlet: `163.253 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 332.578 | 273.120 | 211.609 | 286.222 | 218.297 | 211.063 | 180.792 | 174.604 | 102.292 | 100.361 | 183.728 |
| 1 | 5 | 8 | 298.175 | 250.370 | 194.641 | 261.582 | 192.484 | 193.080 | 165.387 | 160.321 | 93.464 | 93.530 | 164.353 |
| 1 | 10 | 8 | 298.833 | 253.788 | 195.701 | 261.109 | 193.075 | 194.932 | 164.757 | 161.618 | 94.385 | 93.472 | 164.861 |
| 1 | 15 | 8 | 286.559 | 240.052 | 187.879 | 251.132 | 184.297 | 188.021 | 160.170 | 155.153 | 89.769 | 89.590 | 158.318 |
| 1 | 20 | 8 | 286.646 | 242.288 | 191.431 | 250.743 | 183.229 | 185.333 | 159.694 | 157.628 | 89.712 | 89.627 | 157.672 |
| 1 | 25 | 8 | 288.300 | 243.700 | 189.028 | 253.804 | 186.269 | 187.351 | 160.349 | 155.590 | 91.184 | 91.396 | 160.599 |
| 1 | 30 | 8 | 294.976 | 246.234 | 192.512 | 256.347 | 189.981 | 193.403 | 165.465 | 159.700 | 92.602 | 92.259 | 162.856 |
| 1 | 35 | 8 | 303.802 | 248.920 | 195.859 | 261.743 | 192.757 | 193.901 | 165.915 | 161.120 | 94.066 | 94.472 | 165.054 |
| 1 | 40 | 8 | 288.769 | 241.045 | 187.960 | 252.774 | 185.365 | 186.983 | 159.781 | 157.056 | 89.840 | 93.526 | 157.856 |
| 1 | 45 | 8 | 323.767 | 266.866 | 207.714 | 281.721 | 210.450 | 210.460 | 177.385 | 172.203 | 101.821 | 108.535 | 178.950 |
| 1 | 50 | 8 | 329.859 | 268.226 | 214.415 | 284.457 | 210.274 | 214.477 | 183.432 | 179.175 | 102.693 | 102.543 | 183.003 |
| 1 | 55 | 8 | 329.173 | 269.543 | 208.035 | 282.705 | 205.095 | 211.136 | 179.596 | 171.923 | 101.438 | 106.647 | 176.076 |
| 1 | 60 | 8 | 316.953 | 260.529 | 206.002 | 280.347 | 211.924 | 211.050 | 175.694 | 172.082 | 97.476 | 97.241 | 171.682 |
| 1 | 65 | 8 | 331.382 | 273.588 | 211.231 | 286.882 | 214.024 | 210.818 | 178.003 | 173.389 | 101.299 | 100.691 | 178.653 |
| 1 | 70 | 8 | 303.101 | 249.665 | 194.901 | 262.408 | 193.554 | 194.616 | 165.500 | 159.854 | 93.898 | 97.174 | 166.363 |
| 1 | 75 | 8 | 302.585 | 250.856 | 194.696 | 263.727 | 193.366 | 195.505 | 165.510 | 160.186 | 94.505 | 94.774 | 166.168 |
| 1 | 80 | 8 | 301.819 | 249.986 | 193.672 | 261.571 | 193.720 | 195.047 | 166.109 | 162.036 | 93.832 | 93.849 | 167.992 |
| 1 | 85 | 8 | 301.111 | 250.793 | 193.220 | 261.285 | 192.861 | 194.097 | 165.174 | 159.368 | 93.628 | 93.215 | 164.481 |
| 1 | 90 | 8 | 295.255 | 245.057 | 190.740 | 256.134 | 188.698 | 190.293 | 162.111 | 158.127 | 91.679 | 91.981 | 161.953 |
| 1 | 95 | 8 | 304.788 | 253.021 | 195.635 | 266.760 | 195.689 | 197.212 | 168.038 | 162.312 | 94.667 | 93.960 | 166.240 |
| 1 | 100 | 8 | 303.043 | 251.764 | 195.363 | 266.054 | 195.865 | 196.344 | 167.663 | 159.750 | 93.656 | 94.411 | 165.415 |
| 1 | 105 | 8 | 309.469 | 254.931 | 196.665 | 265.384 | 196.542 | 197.976 | 168.024 | 164.269 | 95.312 | 94.503 | 168.004 |
| 1 | 110 | 8 | 302.745 | 251.969 | 193.864 | 261.778 | 192.776 | 195.285 | 166.252 | 160.358 | 93.759 | 93.313 | 165.280 |
| 1 | 115 | 8 | 302.076 | 251.007 | 193.195 | 261.378 | 192.622 | 194.934 | 165.382 | 160.238 | 94.458 | 93.653 | 164.960 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `9` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `155.153 us` (`1.847x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 174.604 | 1.905 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 160.321 | 1.860 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | full_layerlet | 161.618 | 1.849 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 155.153 | 1.847 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 20 | full_layerlet | 157.628 | 1.818 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 25 | full_layerlet | 155.590 | 1.853 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 30 | full_layerlet | 159.700 | 1.847 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 35 | full_layerlet | 161.120 | 1.886 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 157.056 | 1.839 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 45 | full_layerlet | 172.203 | 1.880 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 179.175 | 1.841 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 171.923 | 1.915 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 172.082 | 1.842 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 173.389 | 1.911 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 159.854 | 1.896 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 75 | full_layerlet | 160.186 | 1.889 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 162.036 | 1.863 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 159.368 | 1.889 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 90 | full_layerlet | 158.127 | 1.867 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 95 | full_layerlet | 162.312 | 1.878 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 159.750 | 1.897 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 105 | full_layerlet | 164.269 | 1.884 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 160.358 | 1.888 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 160.238 | 1.885 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
