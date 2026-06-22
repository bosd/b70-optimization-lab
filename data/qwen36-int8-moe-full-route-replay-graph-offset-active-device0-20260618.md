# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `16`.
- Quant out-variant available: `True`.
- Route source: `data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Fused-prologue active-offset-GEMM max abs diff: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `326.280 us`.
- Mean scratch `xpu_fused_moe`: `269.402 us`.
- Mean preallocated staged: `211.147 us`.
- Mean fused-prologue staged: `286.849 us`.
- Mean fused-prologue offset-GEMM staged: `208.180 us`.
- Mean fused-prologue active-offset-GEMM staged: `208.257 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 375.731 | 296.119 | 232.518 | 333.195 | 231.384 | 231.920 | 113.740 | 111.946 | 192.369 |
| 1 | 4 | 8 | 294.731 | 243.521 | 208.920 | 254.654 | 185.390 | 187.309 | 90.085 | 91.598 | 158.241 |
| 1 | 8 | 8 | 325.088 | 269.396 | 209.284 | 282.417 | 211.104 | 203.174 | 99.039 | 97.037 | 169.900 |
| 1 | 12 | 8 | 394.924 | 314.818 | 243.526 | 359.658 | 246.958 | 259.709 | 119.371 | 118.596 | 208.957 |
| 1 | 16 | 8 | 335.057 | 280.628 | 218.166 | 296.041 | 225.155 | 215.951 | 100.776 | 103.636 | 178.677 |
| 1 | 20 | 8 | 314.564 | 261.607 | 203.440 | 272.891 | 199.290 | 202.098 | 94.864 | 96.262 | 167.190 |
| 1 | 24 | 8 | 304.470 | 245.378 | 191.220 | 259.615 | 186.779 | 191.896 | 92.680 | 91.421 | 161.434 |
| 1 | 28 | 8 | 292.682 | 241.982 | 188.588 | 254.873 | 201.562 | 187.309 | 89.684 | 89.580 | 157.664 |
| 1 | 32 | 8 | 290.763 | 244.410 | 189.654 | 255.975 | 185.120 | 186.165 | 90.600 | 90.938 | 156.250 |
| 1 | 36 | 8 | 291.143 | 241.452 | 190.008 | 257.374 | 186.160 | 187.626 | 90.464 | 91.598 | 158.678 |
| 1 | 40 | 8 | 329.176 | 278.637 | 215.675 | 296.546 | 209.737 | 211.812 | 99.216 | 99.107 | 172.318 |
| 1 | 44 | 8 | 338.120 | 271.471 | 210.766 | 288.839 | 206.549 | 204.942 | 101.618 | 101.962 | 175.994 |
| 1 | 48 | 8 | 315.474 | 263.578 | 206.175 | 278.704 | 204.381 | 208.686 | 98.103 | 96.294 | 170.825 |
| 1 | 52 | 8 | 377.504 | 317.164 | 240.048 | 323.279 | 232.882 | 232.060 | 113.974 | 109.699 | 188.568 |
| 1 | 56 | 8 | 314.064 | 261.326 | 200.600 | 276.697 | 199.716 | 203.424 | 94.104 | 94.234 | 166.452 |
| 1 | 60 | 8 | 326.981 | 278.938 | 229.757 | 298.818 | 218.707 | 218.026 | 100.786 | 99.684 | 172.765 |

## Graph Replay Timing

These timings capture each preallocated candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 313.196 |
| 1 | 0 | preallocated_staged | executed | 316.586 |
| 1 | 0 | fused_prologue_staged | executed | 326.318 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 326.115 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 328.133 |
| 1 | 4 | xpu_fused_moe_with_scratch | executed | 173.202 |
| 1 | 4 | preallocated_staged | executed | 174.530 |
| 1 | 4 | fused_prologue_staged | executed | 186.971 |
| 1 | 4 | fused_prologue_offset_gemm | executed | 174.728 |
| 1 | 4 | fused_prologue_active_offset_gemm | executed | 195.952 |
| 1 | 8 | xpu_fused_moe_with_scratch | executed | 163.706 |
| 1 | 8 | preallocated_staged | executed | 164.291 |
| 1 | 8 | fused_prologue_staged | executed | 179.863 |
| 1 | 8 | fused_prologue_offset_gemm | executed | 180.167 |
| 1 | 8 | fused_prologue_active_offset_gemm | executed | 147.363 |
| 1 | 12 | xpu_fused_moe_with_scratch | executed | 310.804 |
| 1 | 12 | preallocated_staged | executed | 321.196 |
| 1 | 12 | fused_prologue_staged | executed | 326.734 |
| 1 | 12 | fused_prologue_offset_gemm | executed | 328.723 |
| 1 | 12 | fused_prologue_active_offset_gemm | executed | 288.493 |
| 1 | 16 | xpu_fused_moe_with_scratch | executed | 175.235 |
| 1 | 16 | preallocated_staged | executed | 176.563 |
| 1 | 16 | fused_prologue_staged | executed | 180.885 |
| 1 | 16 | fused_prologue_offset_gemm | executed | 180.807 |
| 1 | 16 | fused_prologue_active_offset_gemm | executed | 152.594 |
| 1 | 20 | xpu_fused_moe_with_scratch | executed | 323.463 |
| 1 | 20 | preallocated_staged | executed | 328.247 |
| 1 | 20 | fused_prologue_staged | executed | 334.542 |
| 1 | 20 | fused_prologue_offset_gemm | executed | 329.501 |
| 1 | 20 | fused_prologue_active_offset_gemm | executed | 327.634 |
| 1 | 24 | xpu_fused_moe_with_scratch | executed | 175.409 |
| 1 | 24 | preallocated_staged | executed | 172.585 |
| 1 | 24 | fused_prologue_staged | executed | 172.604 |
| 1 | 24 | fused_prologue_offset_gemm | executed | 180.768 |
| 1 | 24 | fused_prologue_active_offset_gemm | executed | 156.478 |
| 1 | 28 | xpu_fused_moe_with_scratch | executed | 166.195 |
| 1 | 28 | preallocated_staged | executed | 166.111 |
| 1 | 28 | fused_prologue_staged | executed | 182.247 |
| 1 | 28 | fused_prologue_offset_gemm | executed | 179.865 |
| 1 | 28 | fused_prologue_active_offset_gemm | executed | 300.113 |
| 1 | 32 | xpu_fused_moe_with_scratch | executed | 315.000 |
| 1 | 32 | preallocated_staged | executed | 316.758 |
| 1 | 32 | fused_prologue_staged | executed | 326.711 |
| 1 | 32 | fused_prologue_offset_gemm | executed | 326.521 |
| 1 | 32 | fused_prologue_active_offset_gemm | executed | 278.551 |
| 1 | 36 | xpu_fused_moe_with_scratch | executed | 165.214 |
| 1 | 36 | preallocated_staged | executed | 165.578 |
| 1 | 36 | fused_prologue_staged | executed | 180.638 |
| 1 | 36 | fused_prologue_offset_gemm | executed | 179.049 |
| 1 | 36 | fused_prologue_active_offset_gemm | executed | 156.621 |
| 1 | 40 | xpu_fused_moe_with_scratch | executed | 312.731 |
| 1 | 40 | preallocated_staged | executed | 312.767 |
| 1 | 40 | fused_prologue_staged | executed | 319.145 |
| 1 | 40 | fused_prologue_offset_gemm | executed | 318.300 |
| 1 | 40 | fused_prologue_active_offset_gemm | executed | 330.938 |
| 1 | 44 | xpu_fused_moe_with_scratch | executed | 173.813 |
| 1 | 44 | preallocated_staged | executed | 174.307 |
| 1 | 44 | fused_prologue_staged | executed | 193.151 |
| 1 | 44 | fused_prologue_offset_gemm | executed | 190.910 |
| 1 | 44 | fused_prologue_active_offset_gemm | executed | 153.572 |
| 1 | 48 | xpu_fused_moe_with_scratch | executed | 175.230 |
| 1 | 48 | preallocated_staged | executed | 190.986 |
| 1 | 48 | fused_prologue_staged | executed | 184.512 |
| 1 | 48 | fused_prologue_offset_gemm | executed | 231.075 |
| 1 | 48 | fused_prologue_active_offset_gemm | executed | 330.736 |
| 1 | 52 | xpu_fused_moe_with_scratch | executed | 331.682 |
| 1 | 52 | preallocated_staged | executed | 328.396 |
| 1 | 52 | fused_prologue_staged | executed | 332.998 |
| 1 | 52 | fused_prologue_offset_gemm | executed | 182.372 |
| 1 | 52 | fused_prologue_active_offset_gemm | executed | 159.429 |
| 1 | 56 | xpu_fused_moe_with_scratch | executed | 170.183 |
| 1 | 56 | preallocated_staged | executed | 178.295 |
| 1 | 56 | fused_prologue_staged | executed | 191.911 |
| 1 | 56 | fused_prologue_offset_gemm | executed | 173.576 |
| 1 | 56 | fused_prologue_active_offset_gemm | executed | 144.851 |
| 1 | 60 | xpu_fused_moe_with_scratch | executed | 324.670 |
| 1 | 60 | preallocated_staged | executed | 331.261 |
| 1 | 60 | fused_prologue_staged | executed | 334.555 |
| 1 | 60 | fused_prologue_offset_gemm | executed | 329.750 |
| 1 | 60 | fused_prologue_active_offset_gemm | executed | 326.716 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `16`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `185.120 us` (`1.571x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_offset_gemm | 231.384 | 1.624 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | fused_prologue_offset_gemm | 185.390 | 1.590 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | fused_prologue_active_offset_gemm | 203.174 | 1.600 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | preallocated_staged | 243.526 | 1.622 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | fused_prologue_active_offset_gemm | 215.951 | 1.552 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | fused_prologue_offset_gemm | 199.290 | 1.578 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | fused_prologue_offset_gemm | 186.779 | 1.630 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | fused_prologue_active_offset_gemm | 187.309 | 1.563 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | fused_prologue_offset_gemm | 185.120 | 1.571 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | fused_prologue_offset_gemm | 186.160 | 1.564 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | fused_prologue_offset_gemm | 209.737 | 1.569 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | fused_prologue_active_offset_gemm | 204.942 | 1.650 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | fused_prologue_offset_gemm | 204.381 | 1.544 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 52 | fused_prologue_active_offset_gemm | 232.060 | 1.627 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | fused_prologue_offset_gemm | 199.716 | 1.573 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | fused_prologue_active_offset_gemm | 218.026 | 1.500 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
