# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `3`.
- Route mode/source: `synthetic_hot_skew`.
- Quant out-variant available: `True`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `235.000`.
- Fused-prologue offset-GEMM max abs diff: `235.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `327.275 us`.
- Mean scratch `xpu_fused_moe`: `265.276 us`.
- Mean preallocated staged: `213.657 us`.
- Mean fused-prologue staged: `283.038 us`.
- Mean fused-prologue offset-GEMM staged: `206.306 us`.
- Mean full C++ layerlet: `176.889 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | None | 12 | 310.875 | 247.208 | 198.094 | 272.954 | 199.570 | n/a | n/a | 178.048 | 94.698 | 94.445 | 171.438 |
| 4 | None | 14 | 350.402 | 287.443 | 233.811 | 300.034 | 215.676 | n/a | n/a | 183.560 | 101.595 | 104.214 | 177.014 |
| 8 | None | 16 | 320.548 | 261.176 | 209.066 | 276.126 | 203.671 | n/a | n/a | 169.058 | 98.456 | 101.166 | 172.439 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 2 | None | xpu_fused_moe_with_scratch | executed | 321.864 |
| 2 | None | preallocated_staged | executed | 328.260 |
| 2 | None | fused_prologue_staged | executed | 334.485 |
| 2 | None | fused_prologue_offset_gemm | executed | 338.328 |
| 2 | None | full_layerlet | executed | 337.753 |
| 4 | None | xpu_fused_moe_with_scratch | executed | 197.158 |
| 4 | None | preallocated_staged | executed | 195.213 |
| 4 | None | fused_prologue_staged | executed | 190.827 |
| 4 | None | fused_prologue_offset_gemm | executed | 192.696 |
| 4 | None | full_layerlet | executed | 193.201 |
| 8 | None | xpu_fused_moe_with_scratch | executed | 182.663 |
| 8 | None | preallocated_staged | executed | 190.263 |
| 8 | None | fused_prologue_staged | executed | 191.656 |
| 8 | None | fused_prologue_offset_gemm | executed | 192.777 |
| 8 | None | full_layerlet | executed | 190.767 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `169.058 us` (`1.896x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 2 | None | full_layerlet | 178.048 | 1.746 | False | best_exact_nonreference_misses_target_layerlet_us |
| 4 | None | full_layerlet | 183.560 | 1.909 | False | best_exact_nonreference_misses_target_layerlet_us |
| 8 | None | full_layerlet | 169.058 | 1.896 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is not exact against `xpu_fused_moe`; do not use it as an endpoint candidate.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
