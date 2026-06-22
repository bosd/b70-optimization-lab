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

- Mean `xpu_fused_moe`: `313.069 us`.
- Mean scratch `xpu_fused_moe`: `258.211 us`.
- Mean prologue-scratch `xpu_fused_moe`: `262.772 us`.
- Mean preallocated staged: `202.034 us`.
- Mean fused-prologue staged: `275.439 us`.
- Mean fused-prologue offset-GEMM staged: `200.341 us`.
- Mean fused-prologue active-offset-GEMM staged: `202.135 us`.
- Mean full C++ layerlet: `170.390 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 297.088 | 243.808 | 248.198 | 190.660 | 259.745 | 189.819 | 191.640 | n/a | 161.367 | 91.102 | 91.435 | 160.909 |
| 1 | 80 | 8 | 293.316 | 244.791 | 248.003 | 191.226 | 257.484 | 188.360 | 190.395 | n/a | 160.552 | 91.234 | 91.297 | 161.569 |
| 1 | 115 | 8 | 348.804 | 286.032 | 292.116 | 224.215 | 309.088 | 222.846 | 224.372 | n/a | 189.252 | 106.266 | 106.863 | 183.804 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 311.373 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 316.719 |
| 1 | 0 | preallocated_staged | executed | 314.101 |
| 1 | 0 | fused_prologue_staged | executed | 320.226 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 322.067 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 313.386 |
| 1 | 0 | full_layerlet | executed | 324.516 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 311.449 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 318.547 |
| 1 | 80 | preallocated_staged | executed | 329.035 |
| 1 | 80 | fused_prologue_staged | executed | 334.095 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 329.246 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 334.329 |
| 1 | 80 | full_layerlet | executed | 187.273 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 331.162 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 329.514 |
| 1 | 115 | preallocated_staged | executed | 323.547 |
| 1 | 115 | fused_prologue_staged | executed | 332.985 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 328.695 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 325.827 |
| 1 | 115 | full_layerlet | executed | 333.889 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `160.552 us` (`1.827x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 161.367 | 1.841 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 160.552 | 1.827 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 189.252 | 1.843 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
