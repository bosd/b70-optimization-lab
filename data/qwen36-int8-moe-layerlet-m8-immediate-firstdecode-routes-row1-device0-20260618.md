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

- Mean `xpu_fused_moe`: `311.433 us`.
- Mean scratch `xpu_fused_moe`: `259.222 us`.
- Mean preallocated staged: `199.995 us`.
- Mean fused-prologue staged: `270.547 us`.
- Mean fused-prologue offset-GEMM staged: `199.141 us`.
- Mean fused-prologue active-offset-GEMM staged: `199.693 us`.
- Mean fused-prologue middle-layerlet staged: `171.001 us`.
- Mean full C++ layerlet: `167.267 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 392.012 | 328.326 | 248.517 | 335.594 | 257.774 | 247.523 | 211.194 | 212.484 | 119.342 | 122.215 | 216.540 |
| 1 | 5 | 8 | 313.009 | 260.701 | 200.694 | 273.486 | 205.264 | 201.302 | 172.762 | 167.044 | 97.641 | 96.745 | 172.061 |
| 1 | 10 | 8 | 300.870 | 251.670 | 194.384 | 262.255 | 193.689 | 194.311 | 166.590 | 161.715 | 94.222 | 94.734 | 165.502 |
| 1 | 15 | 8 | 316.245 | 263.285 | 204.479 | 273.522 | 201.399 | 203.938 | 173.153 | 169.445 | 97.325 | 96.897 | 174.991 |
| 1 | 20 | 8 | 287.717 | 237.972 | 184.589 | 251.059 | 184.137 | 185.005 | 158.021 | 155.582 | 90.415 | 89.234 | 158.061 |
| 1 | 25 | 8 | 285.219 | 239.070 | 186.363 | 251.023 | 183.158 | 184.774 | 158.740 | 155.552 | 89.436 | 89.542 | 158.910 |
| 1 | 30 | 8 | 327.080 | 270.708 | 207.495 | 282.884 | 208.611 | 206.738 | 176.962 | 171.955 | 99.455 | 100.668 | 172.674 |
| 1 | 35 | 8 | 303.828 | 250.512 | 193.936 | 263.340 | 192.554 | 193.554 | 165.814 | 160.378 | 93.882 | 93.224 | 164.457 |
| 1 | 40 | 8 | 326.557 | 270.623 | 207.635 | 282.168 | 207.493 | 208.234 | 177.729 | 174.000 | 99.434 | 101.865 | 179.279 |
| 1 | 45 | 8 | 314.316 | 262.904 | 202.293 | 272.479 | 200.226 | 201.523 | 172.224 | 166.186 | 96.762 | 96.710 | 171.064 |
| 1 | 50 | 8 | 319.335 | 264.175 | 205.240 | 278.005 | 207.345 | 205.684 | 175.774 | 173.635 | 98.214 | 98.832 | 173.979 |
| 1 | 55 | 8 | 286.875 | 238.745 | 186.646 | 251.399 | 183.234 | 184.123 | 158.502 | 155.977 | 89.696 | 89.566 | 158.075 |
| 1 | 60 | 8 | 303.951 | 253.800 | 195.372 | 263.186 | 193.733 | 197.194 | 167.365 | 163.753 | 94.186 | 94.993 | 165.455 |
| 1 | 65 | 8 | 303.738 | 250.349 | 193.821 | 262.394 | 192.773 | 194.233 | 165.627 | 161.036 | 93.580 | 93.484 | 165.241 |
| 1 | 70 | 8 | 301.151 | 249.953 | 192.691 | 260.906 | 192.524 | 192.687 | 164.384 | 160.226 | 93.953 | 93.219 | 164.896 |
| 1 | 75 | 8 | 314.455 | 264.240 | 204.076 | 272.684 | 199.392 | 202.045 | 173.960 | 168.465 | 97.502 | 97.424 | 174.337 |
| 1 | 80 | 8 | 302.151 | 248.007 | 191.634 | 258.191 | 187.812 | 188.755 | 163.205 | 160.700 | 92.505 | 93.682 | 162.840 |
| 1 | 85 | 8 | 285.903 | 237.236 | 185.721 | 249.932 | 183.311 | 183.439 | 158.372 | 155.325 | 88.873 | 89.106 | 158.191 |
| 1 | 90 | 8 | 286.647 | 239.000 | 185.858 | 249.861 | 182.017 | 183.839 | 158.351 | 155.094 | 89.014 | 89.342 | 156.871 |
| 1 | 95 | 8 | 286.052 | 238.991 | 184.290 | 249.977 | 182.080 | 183.837 | 158.217 | 154.731 | 89.450 | 89.550 | 156.951 |
| 1 | 100 | 8 | 311.181 | 257.962 | 198.170 | 268.526 | 196.479 | 199.396 | 171.620 | 168.953 | 97.049 | 97.543 | 170.198 |
| 1 | 105 | 8 | 355.747 | 296.099 | 227.568 | 311.844 | 228.906 | 230.828 | 196.896 | 193.010 | 109.427 | 106.750 | 190.479 |
| 1 | 110 | 8 | 316.953 | 259.616 | 200.134 | 273.222 | 199.351 | 203.705 | 172.873 | 169.642 | 96.578 | 96.783 | 170.071 |
| 1 | 115 | 8 | 333.396 | 287.373 | 218.271 | 295.200 | 216.127 | 215.965 | 185.681 | 179.523 | 103.691 | 103.481 | 180.573 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `6` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `154.731 us` (`1.849x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_middle_layerlet | 211.194 | 1.856 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 167.044 | 1.874 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | full_layerlet | 161.715 | 1.860 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 169.445 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 155.582 | 1.849 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 25 | full_layerlet | 155.552 | 1.834 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 30 | full_layerlet | 171.955 | 1.902 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 35 | full_layerlet | 160.378 | 1.894 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 174.000 | 1.877 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 45 | full_layerlet | 166.186 | 1.891 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 173.635 | 1.839 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 155.977 | 1.839 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 60 | full_layerlet | 163.753 | 1.856 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 161.036 | 1.886 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 160.226 | 1.880 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 75 | full_layerlet | 168.465 | 1.867 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 160.700 | 1.880 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 155.325 | 1.841 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 90 | full_layerlet | 155.094 | 1.848 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 95 | full_layerlet | 154.731 | 1.849 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 100 | full_layerlet | 168.953 | 1.842 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 105 | full_layerlet | 193.010 | 1.843 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 169.642 | 1.868 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 179.523 | 1.857 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
