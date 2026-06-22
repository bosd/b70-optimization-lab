# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `7`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `285`; top-k rows loaded: `285`.
- Route start indices: `0,40,80,85,95,100,115`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Prologue-scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Fused-prologue active-offset-GEMM max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `329.726 us`.
- Mean scratch `xpu_fused_moe`: `267.706 us`.
- Mean prologue-scratch `xpu_fused_moe`: `272.695 us`.
- Mean preallocated staged: `213.375 us`.
- Mean fused-prologue staged: `287.782 us`.
- Mean fused-prologue offset-GEMM staged: `210.145 us`.
- Mean fused-prologue active-offset-GEMM staged: `213.908 us`.
- Mean full C++ layerlet: `177.902 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 354.350 | 294.266 | 299.238 | 232.716 | 312.655 | 228.601 | 233.165 | n/a | 193.652 | 106.839 | 107.201 | 186.459 |
| 1 | 40 | 8 | 313.023 | 258.471 | 262.252 | 202.504 | 273.530 | 198.927 | 204.005 | n/a | 169.306 | 95.200 | 94.360 | 166.820 |
| 1 | 80 | 8 | 335.281 | 275.019 | 282.607 | 219.075 | 295.064 | 213.362 | 215.743 | n/a | 181.801 | 101.631 | 100.925 | 175.670 |
| 1 | 85 | 8 | 304.131 | 251.348 | 254.118 | 196.421 | 265.188 | 192.569 | 195.985 | n/a | 162.998 | 92.687 | 93.862 | 163.230 |
| 1 | 95 | 8 | 352.524 | 277.763 | 285.850 | 223.777 | 302.856 | 222.822 | 225.642 | n/a | 188.187 | 104.239 | 103.679 | 181.059 |
| 1 | 100 | 8 | 327.088 | 268.080 | 272.855 | 211.227 | 285.129 | 209.157 | 213.115 | n/a | 175.806 | 96.799 | 96.462 | 169.628 |
| 1 | 115 | 8 | 321.683 | 248.995 | 251.945 | 207.902 | 280.050 | 205.580 | 209.699 | n/a | 173.560 | 96.500 | 96.191 | 169.270 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 337.258 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 336.631 |
| 1 | 0 | preallocated_staged | executed | 239.685 |
| 1 | 0 | fused_prologue_staged | executed | 187.133 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 192.374 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 161.177 |
| 1 | 0 | full_layerlet | executed | 177.003 |
| 1 | 40 | xpu_fused_moe_with_scratch | executed | 319.757 |
| 1 | 40 | xpu_fused_moe_with_prologue_scratch | executed | 330.096 |
| 1 | 40 | preallocated_staged | executed | 329.750 |
| 1 | 40 | fused_prologue_staged | executed | 335.459 |
| 1 | 40 | fused_prologue_offset_gemm | executed | 268.215 |
| 1 | 40 | fused_prologue_active_offset_gemm | executed | 150.860 |
| 1 | 40 | full_layerlet | executed | 173.613 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 320.233 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 209.494 |
| 1 | 80 | preallocated_staged | executed | 164.391 |
| 1 | 80 | fused_prologue_staged | executed | 171.702 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 179.586 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 149.765 |
| 1 | 80 | full_layerlet | executed | 176.535 |
| 1 | 85 | xpu_fused_moe_with_scratch | executed | 262.981 |
| 1 | 85 | xpu_fused_moe_with_prologue_scratch | executed | 181.714 |
| 1 | 85 | preallocated_staged | executed | 180.924 |
| 1 | 85 | fused_prologue_staged | executed | 191.203 |
| 1 | 85 | fused_prologue_offset_gemm | executed | 182.621 |
| 1 | 85 | fused_prologue_active_offset_gemm | executed | 177.479 |
| 1 | 85 | full_layerlet | executed | 181.378 |
| 1 | 95 | xpu_fused_moe_with_scratch | executed | 318.386 |
| 1 | 95 | xpu_fused_moe_with_prologue_scratch | executed | 326.370 |
| 1 | 95 | preallocated_staged | executed | 226.539 |
| 1 | 95 | fused_prologue_staged | executed | 177.664 |
| 1 | 95 | fused_prologue_offset_gemm | executed | 171.232 |
| 1 | 95 | fused_prologue_active_offset_gemm | executed | 154.948 |
| 1 | 95 | full_layerlet | executed | 173.792 |
| 1 | 100 | xpu_fused_moe_with_scratch | executed | 317.752 |
| 1 | 100 | xpu_fused_moe_with_prologue_scratch | executed | 324.661 |
| 1 | 100 | preallocated_staged | executed | 334.029 |
| 1 | 100 | fused_prologue_staged | executed | 335.898 |
| 1 | 100 | fused_prologue_offset_gemm | executed | 302.357 |
| 1 | 100 | fused_prologue_active_offset_gemm | executed | 159.469 |
| 1 | 100 | full_layerlet | executed | 173.525 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 326.580 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 340.599 |
| 1 | 115 | preallocated_staged | executed | 220.641 |
| 1 | 115 | fused_prologue_staged | executed | 192.441 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 176.733 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 155.179 |
| 1 | 115 | full_layerlet | executed | 188.705 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `162.998 us` (`1.866x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 193.652 | 1.830 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 169.306 | 1.849 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 181.801 | 1.844 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 162.998 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 188.187 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 175.806 | 1.861 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 173.560 | 1.853 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
