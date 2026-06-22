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
- Fused-prologue middle-layerlet max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `327.487 us`.
- Mean scratch `xpu_fused_moe`: `270.806 us`.
- Mean preallocated staged: `211.280 us`.
- Mean fused-prologue staged: `287.226 us`.
- Mean fused-prologue offset-GEMM staged: `207.317 us`.
- Mean fused-prologue middle-layerlet staged: `179.627 us`.
- Mean full C++ layerlet: `175.198 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 300.222 | 251.368 | 190.857 | 262.115 | 190.112 | n/a | 162.829 | 189.332 | 91.607 | 94.380 | 173.143 |
| 1 | 5 | 8 | 299.780 | 245.267 | 192.747 | 258.362 | 186.654 | n/a | 175.353 | 156.321 | 92.595 | 90.220 | 160.307 |
| 1 | 10 | 8 | 296.175 | 250.397 | 189.263 | 260.225 | 188.379 | n/a | 162.231 | 160.871 | 98.835 | 93.097 | 153.227 |
| 1 | 15 | 8 | 297.345 | 247.407 | 189.315 | 260.832 | 191.438 | n/a | 163.739 | 160.836 | 89.527 | 90.281 | 162.699 |
| 1 | 20 | 8 | 297.934 | 256.915 | 203.857 | 277.810 | 201.968 | n/a | 174.789 | 167.362 | 89.995 | 89.709 | 163.219 |
| 1 | 25 | 8 | 315.761 | 261.326 | 202.783 | 274.655 | 202.185 | n/a | 169.399 | 165.759 | 93.921 | 99.173 | 171.903 |
| 1 | 30 | 8 | 300.265 | 247.217 | 189.757 | 258.093 | 185.969 | n/a | 162.084 | 160.238 | 91.503 | 90.688 | 158.973 |
| 1 | 35 | 8 | 386.455 | 317.018 | 265.365 | 358.765 | 246.133 | n/a | 209.127 | 205.331 | 114.807 | 113.958 | 198.926 |
| 1 | 40 | 8 | 294.268 | 244.695 | 188.335 | 259.168 | 189.193 | n/a | 161.876 | 156.520 | 89.587 | 90.853 | 158.912 |
| 1 | 45 | 8 | 314.349 | 267.237 | 255.684 | 314.513 | 203.216 | n/a | 183.976 | 179.400 | 95.021 | 98.514 | 170.768 |
| 1 | 50 | 8 | 350.246 | 283.885 | 222.447 | 302.631 | 220.151 | n/a | 191.525 | 179.530 | 108.845 | 110.231 | 190.701 |
| 1 | 55 | 8 | 367.293 | 300.213 | 228.228 | 319.367 | 228.219 | n/a | 195.676 | 190.207 | 109.139 | 110.240 | 197.747 |
| 1 | 60 | 8 | 319.011 | 263.579 | 198.961 | 277.255 | 207.818 | n/a | 171.236 | 170.291 | 95.767 | 97.318 | 167.951 |
| 1 | 65 | 8 | 430.525 | 341.432 | 248.638 | 341.935 | 248.603 | n/a | 234.208 | 220.220 | 120.267 | 117.763 | 206.527 |
| 1 | 70 | 8 | 388.657 | 320.008 | 243.091 | 338.771 | 241.497 | n/a | 209.699 | 199.394 | 112.693 | 112.138 | 196.881 |
| 1 | 75 | 8 | 375.951 | 322.443 | 247.139 | 337.437 | 254.523 | n/a | 222.135 | 205.253 | 111.523 | 112.216 | 197.799 |
| 1 | 80 | 8 | 334.195 | 267.202 | 214.630 | 291.191 | 209.465 | n/a | 179.773 | 172.224 | 98.081 | 96.989 | 189.176 |
| 1 | 85 | 8 | 362.215 | 283.209 | 219.986 | 298.853 | 218.322 | n/a | 185.025 | 184.843 | 105.742 | 104.156 | 188.916 |
| 1 | 90 | 8 | 296.521 | 244.296 | 192.270 | 257.972 | 185.640 | n/a | 162.075 | 161.850 | 89.509 | 89.041 | 159.744 |
| 1 | 95 | 8 | 340.444 | 297.804 | 223.626 | 309.374 | 222.595 | n/a | 189.081 | 188.292 | 100.767 | 100.793 | 174.902 |
| 1 | 100 | 8 | 298.419 | 245.466 | 191.377 | 258.544 | 189.696 | n/a | 161.477 | 155.307 | 92.499 | 90.593 | 158.730 |
| 1 | 105 | 8 | 295.247 | 246.298 | 191.230 | 259.757 | 185.640 | n/a | 164.389 | 156.113 | 91.243 | 90.393 | 161.850 |
| 1 | 110 | 8 | 297.613 | 249.331 | 189.072 | 258.570 | 191.005 | n/a | 159.683 | 160.637 | 89.605 | 90.471 | 158.947 |
| 1 | 115 | 8 | 300.803 | 245.327 | 192.053 | 257.235 | 187.191 | n/a | 159.666 | 158.617 | 89.501 | 89.995 | 159.406 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `6` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `155.307 us` (`1.921x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_middle_layerlet | 162.829 | 1.844 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 156.321 | 1.918 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 10 | full_layerlet | 160.871 | 1.841 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 160.836 | 1.849 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 167.362 | 1.780 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 25 | full_layerlet | 165.759 | 1.905 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 30 | full_layerlet | 160.238 | 1.874 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 35 | full_layerlet | 205.331 | 1.882 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 156.520 | 1.880 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 45 | full_layerlet | 179.400 | 1.752 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 179.530 | 1.951 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 190.207 | 1.931 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 170.291 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 220.220 | 1.955 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 199.394 | 1.949 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 75 | full_layerlet | 205.253 | 1.832 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 172.224 | 1.940 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 184.843 | 1.960 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 161.850 | 1.832 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 188.292 | 1.808 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 155.307 | 1.921 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 105 | full_layerlet | 156.113 | 1.891 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 110 | fused_prologue_middle_layerlet | 159.683 | 1.864 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 115 | full_layerlet | 158.617 | 1.896 | True | candidate_layerlet_meets_speed_and_exactness_gate |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
