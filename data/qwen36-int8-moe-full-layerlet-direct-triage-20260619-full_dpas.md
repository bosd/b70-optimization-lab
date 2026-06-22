# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `3`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `285`; top-k rows loaded: `285`.
- Route start indices: `0,80,115`.
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

- Mean `xpu_fused_moe`: `304.712 us`.
- Mean scratch `xpu_fused_moe`: `249.992 us`.
- Mean prologue-scratch `xpu_fused_moe`: `255.555 us`.
- Mean preallocated staged: `196.764 us`.
- Mean fused-prologue staged: `265.546 us`.
- Mean fused-prologue offset-GEMM staged: `194.227 us`.
- Mean fused-prologue active-offset-GEMM staged: `196.304 us`.
- Mean full C++ layerlet: `165.611 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 307.071 | 249.163 | 253.272 | 197.132 | 265.133 | 193.511 | 194.419 | n/a | 164.406 | 91.893 | 94.654 | 162.942 |
| 1 | 80 | 8 | 311.948 | 255.506 | 264.767 | 202.490 | 273.026 | 199.896 | 203.527 | n/a | 171.804 | 95.767 | 95.175 | 166.948 |
| 1 | 115 | 8 | 295.118 | 245.307 | 248.627 | 190.670 | 258.478 | 189.274 | 190.967 | n/a | 160.624 | 90.601 | 91.213 | 159.461 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 311.971 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 320.497 |
| 1 | 0 | preallocated_staged | executed | 313.035 |
| 1 | 0 | fused_prologue_staged | executed | 319.592 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 319.423 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 305.282 |
| 1 | 0 | full_layerlet | executed | 321.597 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 315.190 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 317.910 |
| 1 | 80 | preallocated_staged | executed | 310.996 |
| 1 | 80 | fused_prologue_staged | executed | 322.041 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 318.698 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 223.038 |
| 1 | 80 | full_layerlet | executed | 183.453 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 309.083 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 314.337 |
| 1 | 115 | preallocated_staged | executed | 312.200 |
| 1 | 115 | fused_prologue_staged | executed | 320.354 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 321.612 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 178.747 |
| 1 | 115 | full_layerlet | executed | 177.050 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `160.624 us` (`1.837x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 164.406 | 1.868 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 171.804 | 1.816 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 160.624 | 1.837 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
