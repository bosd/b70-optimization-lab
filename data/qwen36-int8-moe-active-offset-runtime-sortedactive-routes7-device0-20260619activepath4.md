# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `5`.
- Route mode/source: `synthetic_uniform`.
- Quant out-variant available: `True`.
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

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `329.811 us`.
- Mean scratch `xpu_fused_moe`: `281.834 us`.
- Mean prologue-scratch `xpu_fused_moe`: `282.249 us`.
- Mean preallocated staged: `234.391 us`.
- Mean fused-prologue staged: `305.147 us`.
- Mean fused-prologue offset-GEMM staged: `233.309 us`.
- Mean fused-prologue active-offset-GEMM staged: `225.327 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | None | 8 | 313.936 | 260.569 | 281.095 | 204.733 | 278.641 | 205.766 | 202.420 | n/a | n/a | 100.069 | 99.225 | 175.778 |
| 2 | None | 16 | 292.384 | 244.362 | 238.996 | 193.790 | 257.695 | 189.755 | 191.344 | n/a | n/a | 93.282 | 92.410 | 163.134 |
| 4 | None | 32 | 325.838 | 265.835 | 259.165 | 206.917 | 283.390 | 206.088 | 210.181 | n/a | n/a | 98.504 | 99.653 | 172.070 |
| 8 | None | 64 | 312.309 | 273.458 | 271.677 | 237.417 | 301.021 | 237.142 | 212.569 | n/a | n/a | 113.181 | 96.015 | 169.019 |
| 16 | None | 128 | 404.589 | 364.948 | 360.313 | 329.099 | 404.986 | 327.791 | 310.119 | n/a | n/a | 169.491 | 115.891 | 182.339 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | None | xpu_fused_moe_with_scratch | executed | 322.670 |
| 1 | None | xpu_fused_moe_with_prologue_scratch | executed | 320.776 |
| 1 | None | preallocated_staged | executed | 328.007 |
| 1 | None | fused_prologue_staged | executed | 337.035 |
| 1 | None | fused_prologue_offset_gemm | executed | 333.762 |
| 1 | None | fused_prologue_active_offset_gemm | executed | 202.088 |
| 2 | None | xpu_fused_moe_with_scratch | executed | 333.223 |
| 2 | None | xpu_fused_moe_with_prologue_scratch | executed | 336.608 |
| 2 | None | preallocated_staged | executed | 341.449 |
| 2 | None | fused_prologue_staged | executed | 350.182 |
| 2 | None | fused_prologue_offset_gemm | executed | 261.912 |
| 2 | None | fused_prologue_active_offset_gemm | executed | 177.811 |
| 4 | None | xpu_fused_moe_with_scratch | executed | 341.032 |
| 4 | None | xpu_fused_moe_with_prologue_scratch | executed | 358.072 |
| 4 | None | preallocated_staged | executed | 356.814 |
| 4 | None | fused_prologue_staged | executed | 231.585 |
| 4 | None | fused_prologue_offset_gemm | executed | 222.827 |
| 4 | None | fused_prologue_active_offset_gemm | executed | 178.669 |
| 8 | None | xpu_fused_moe_with_scratch | executed | 405.297 |
| 8 | None | xpu_fused_moe_with_prologue_scratch | executed | 405.049 |
| 8 | None | preallocated_staged | executed | 303.077 |
| 8 | None | fused_prologue_staged | executed | 283.076 |
| 8 | None | fused_prologue_offset_gemm | executed | 281.972 |
| 8 | None | fused_prologue_active_offset_gemm | executed | 240.795 |
| 16 | None | xpu_fused_moe_with_scratch | executed | 500.093 |
| 16 | None | xpu_fused_moe_with_prologue_scratch | executed | 496.805 |
| 16 | None | preallocated_staged | executed | 498.923 |
| 16 | None | fused_prologue_staged | executed | 515.199 |
| 16 | None | fused_prologue_offset_gemm | executed | 503.128 |
| 16 | None | fused_prologue_active_offset_gemm | executed | 335.813 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `5`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `189.755 us` (`1.541x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | None | fused_prologue_active_offset_gemm | 202.420 | 1.551 | False | best_exact_nonreference_misses_target_layerlet_us |
| 2 | None | fused_prologue_offset_gemm | 189.755 | 1.541 | False | best_exact_nonreference_misses_target_layerlet_us |
| 4 | None | fused_prologue_offset_gemm | 206.088 | 1.581 | False | best_exact_nonreference_misses_target_layerlet_us |
| 8 | None | fused_prologue_active_offset_gemm | 212.569 | 1.469 | False | best_exact_nonreference_misses_target_layerlet_us |
| 16 | None | fused_prologue_active_offset_gemm | 310.119 | 1.305 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
