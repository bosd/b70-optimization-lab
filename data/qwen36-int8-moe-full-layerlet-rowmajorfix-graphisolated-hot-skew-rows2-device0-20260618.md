# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `1`.
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

- Mean `xpu_fused_moe`: `331.162 us`.
- Mean scratch `xpu_fused_moe`: `273.208 us`.
- Mean preallocated staged: `212.400 us`.
- Mean fused-prologue staged: `285.077 us`.
- Mean fused-prologue offset-GEMM staged: `208.858 us`.
- Mean full C++ layerlet: `176.956 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | None | 12 | 331.162 | 273.208 | 212.400 | 285.077 | 208.858 | n/a | n/a | 176.956 | 97.552 | 97.539 | 173.030 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 2 | None | xpu_fused_moe_with_scratch | executed | 318.162 |
| 2 | None | preallocated_staged | executed | 319.111 |
| 2 | None | fused_prologue_staged | executed | 327.530 |
| 2 | None | fused_prologue_offset_gemm | executed | 326.004 |
| 2 | None | full_layerlet | executed | 324.782 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `1`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `176.956 us` (`1.871x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 2 | None | full_layerlet | 176.956 | 1.871 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is not exact against `xpu_fused_moe`; do not use it as an endpoint candidate.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
