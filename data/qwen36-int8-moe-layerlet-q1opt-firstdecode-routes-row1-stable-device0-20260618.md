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

- Mean `xpu_fused_moe`: `325.996 us`.
- Mean scratch `xpu_fused_moe`: `268.252 us`.
- Mean preallocated staged: `208.362 us`.
- Mean fused-prologue staged: `282.791 us`.
- Mean fused-prologue offset-GEMM staged: `206.892 us`.
- Mean fused-prologue active-offset-GEMM staged: `208.903 us`.
- Mean fused-prologue middle-layerlet staged: `176.094 us`.
- Mean full C++ layerlet: `171.950 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 326.123 | 267.292 | 210.174 | 281.225 | 222.120 | 206.547 | 175.264 | 172.585 | 96.082 | 100.946 | 173.068 |
| 1 | 5 | 8 | 305.457 | 251.836 | 196.414 | 264.727 | 193.409 | 198.373 | 166.866 | 163.554 | 93.222 | 93.754 | 167.296 |
| 1 | 10 | 8 | 319.460 | 262.583 | 206.485 | 278.212 | 205.076 | 204.859 | 174.531 | 170.085 | 99.629 | 102.365 | 175.273 |
| 1 | 15 | 8 | 298.716 | 246.685 | 194.012 | 260.185 | 190.304 | 192.859 | 167.265 | 161.301 | 93.577 | 93.539 | 167.787 |
| 1 | 20 | 8 | 309.280 | 254.086 | 197.780 | 270.026 | 195.380 | 198.813 | 169.045 | 164.630 | 95.654 | 93.508 | 165.753 |
| 1 | 25 | 8 | 324.159 | 265.964 | 207.490 | 280.537 | 205.450 | 207.139 | 173.677 | 167.211 | 96.254 | 96.444 | 169.329 |
| 1 | 30 | 8 | 337.118 | 283.932 | 214.568 | 290.500 | 209.314 | 216.349 | 183.473 | 182.211 | 102.057 | 101.641 | 179.693 |
| 1 | 35 | 8 | 320.944 | 267.082 | 204.923 | 278.639 | 202.001 | 205.995 | 172.850 | 170.154 | 95.761 | 98.022 | 166.688 |
| 1 | 40 | 8 | 362.868 | 296.521 | 230.038 | 320.580 | 228.308 | 231.171 | 195.610 | 195.133 | 107.768 | 106.586 | 185.364 |
| 1 | 45 | 8 | 325.033 | 269.031 | 210.125 | 280.216 | 203.403 | 206.582 | 176.613 | 172.278 | 98.512 | 99.025 | 172.224 |
| 1 | 50 | 8 | 384.256 | 310.346 | 244.908 | 326.548 | 237.661 | 241.271 | 201.393 | 199.455 | 113.807 | 111.790 | 195.894 |
| 1 | 55 | 8 | 375.913 | 308.022 | 235.830 | 329.631 | 241.153 | 240.101 | 203.942 | 197.997 | 112.438 | 109.488 | 194.411 |
| 1 | 60 | 8 | 372.233 | 306.880 | 231.197 | 322.585 | 236.016 | 236.905 | 194.171 | 190.830 | 108.755 | 108.358 | 193.915 |
| 1 | 65 | 8 | 316.841 | 261.690 | 204.726 | 276.245 | 204.301 | 206.291 | 172.715 | 166.178 | 94.004 | 97.947 | 166.081 |
| 1 | 70 | 8 | 317.467 | 262.361 | 203.003 | 276.510 | 202.164 | 205.142 | 172.494 | 165.445 | 94.661 | 94.524 | 166.570 |
| 1 | 75 | 8 | 311.919 | 254.850 | 198.290 | 267.367 | 194.749 | 197.441 | 167.345 | 162.171 | 92.725 | 93.025 | 164.547 |
| 1 | 80 | 8 | 311.393 | 253.342 | 198.366 | 270.033 | 195.927 | 200.588 | 168.461 | 169.120 | 92.026 | 92.870 | 163.968 |
| 1 | 85 | 8 | 320.500 | 262.193 | 203.660 | 275.671 | 202.225 | 204.171 | 170.929 | 166.469 | 94.247 | 94.165 | 166.747 |
| 1 | 90 | 8 | 319.290 | 260.886 | 203.753 | 276.416 | 202.218 | 205.875 | 170.889 | 164.398 | 94.082 | 93.895 | 166.431 |
| 1 | 95 | 8 | 319.691 | 262.009 | 205.072 | 277.172 | 204.327 | 205.930 | 172.637 | 166.882 | 94.288 | 95.526 | 168.454 |
| 1 | 100 | 8 | 318.238 | 263.663 | 204.303 | 277.131 | 203.585 | 206.333 | 171.889 | 167.989 | 94.630 | 94.562 | 166.154 |
| 1 | 105 | 8 | 319.845 | 262.175 | 205.150 | 276.952 | 203.752 | 206.494 | 171.895 | 166.934 | 95.281 | 95.449 | 167.154 |
| 1 | 110 | 8 | 310.558 | 257.929 | 199.188 | 270.284 | 195.185 | 198.252 | 170.030 | 164.434 | 93.454 | 94.224 | 165.578 |
| 1 | 115 | 8 | 296.611 | 246.683 | 191.242 | 259.587 | 187.385 | 190.192 | 162.266 | 159.356 | 89.468 | 90.709 | 158.449 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `1` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `159.356 us` (`1.861x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 172.585 | 1.890 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 163.554 | 1.868 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | full_layerlet | 170.085 | 1.878 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 161.301 | 1.852 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 164.630 | 1.879 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 25 | full_layerlet | 167.211 | 1.939 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 30 | full_layerlet | 182.211 | 1.850 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 35 | full_layerlet | 170.154 | 1.886 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 195.133 | 1.860 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 45 | full_layerlet | 172.278 | 1.887 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 199.455 | 1.927 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 197.997 | 1.899 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 190.830 | 1.951 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 166.178 | 1.907 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 165.445 | 1.919 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 75 | full_layerlet | 162.171 | 1.923 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | fused_prologue_middle_layerlet | 168.461 | 1.848 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 166.469 | 1.925 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 164.398 | 1.942 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 166.882 | 1.916 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 167.989 | 1.894 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 105 | full_layerlet | 166.934 | 1.916 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 164.434 | 1.889 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 159.356 | 1.861 | True | candidate_layerlet_meets_speed_and_exactness_gate |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
