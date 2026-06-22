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

- Mean `xpu_fused_moe`: `348.283 us`.
- Mean scratch `xpu_fused_moe`: `287.257 us`.
- Mean prologue-scratch `xpu_fused_moe`: `295.338 us`.
- Mean preallocated staged: `227.329 us`.
- Mean fused-prologue staged: `303.952 us`.
- Mean fused-prologue offset-GEMM staged: `221.193 us`.
- Mean fused-prologue active-offset-GEMM staged: `224.125 us`.
- Mean full C++ layerlet: `186.644 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 351.878 | 290.834 | 303.132 | 230.231 | 307.650 | 223.938 | 223.634 | n/a | 188.602 | 103.894 | 102.810 | 181.446 |
| 1 | 80 | 8 | 343.596 | 281.687 | 289.069 | 223.934 | 298.871 | 217.083 | 222.137 | n/a | 183.874 | 101.171 | 101.938 | 178.654 |
| 1 | 115 | 8 | 349.374 | 289.251 | 293.814 | 227.821 | 305.336 | 222.557 | 226.604 | n/a | 187.457 | 104.526 | 105.638 | 181.095 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 315.539 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 321.425 |
| 1 | 0 | preallocated_staged | executed | 311.912 |
| 1 | 0 | fused_prologue_staged | executed | 328.614 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 287.336 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 190.830 |
| 1 | 0 | full_layerlet | executed | 182.029 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 328.175 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 331.534 |
| 1 | 80 | preallocated_staged | executed | 328.182 |
| 1 | 80 | fused_prologue_staged | executed | 344.261 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 335.852 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 328.744 |
| 1 | 80 | full_layerlet | executed | 328.201 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 337.103 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 329.883 |
| 1 | 115 | preallocated_staged | executed | 324.613 |
| 1 | 115 | fused_prologue_staged | executed | 334.108 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 327.891 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 324.665 |
| 1 | 115 | full_layerlet | executed | 329.963 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `183.874 us` (`1.869x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 188.602 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 183.874 | 1.869 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 187.457 | 1.864 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
