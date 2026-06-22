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

- Mean `xpu_fused_moe`: `337.904 us`.
- Mean scratch `xpu_fused_moe`: `278.378 us`.
- Mean prologue-scratch `xpu_fused_moe`: `281.096 us`.
- Mean preallocated staged: `216.135 us`.
- Mean fused-prologue staged: `296.539 us`.
- Mean fused-prologue offset-GEMM staged: `214.330 us`.
- Mean fused-prologue active-offset-GEMM staged: `216.559 us`.
- Mean full C++ layerlet: `181.730 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 349.737 | 286.252 | 287.634 | 224.438 | 309.014 | 220.184 | 223.094 | n/a | 186.594 | 106.191 | 108.091 | 185.870 |
| 1 | 80 | 8 | 338.680 | 280.098 | 284.301 | 216.892 | 298.288 | 216.238 | 216.877 | n/a | 183.581 | 100.661 | 102.919 | 180.620 |
| 1 | 115 | 8 | 325.293 | 268.784 | 271.355 | 207.075 | 282.315 | 206.569 | 209.705 | n/a | 175.014 | 98.346 | 99.682 | 173.520 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 340.626 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 332.917 |
| 1 | 0 | preallocated_staged | executed | 326.381 |
| 1 | 0 | fused_prologue_staged | executed | 334.693 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 228.961 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 172.637 |
| 1 | 0 | full_layerlet | executed | 180.783 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 313.667 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 318.955 |
| 1 | 80 | preallocated_staged | executed | 312.421 |
| 1 | 80 | fused_prologue_staged | executed | 320.434 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 317.000 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 299.198 |
| 1 | 80 | full_layerlet | executed | 316.446 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 309.647 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 316.378 |
| 1 | 115 | preallocated_staged | executed | 313.752 |
| 1 | 115 | fused_prologue_staged | executed | 331.601 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 333.520 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 330.187 |
| 1 | 115 | full_layerlet | executed | 340.207 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `175.014 us` (`1.859x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 186.594 | 1.874 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 183.581 | 1.845 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 175.014 | 1.859 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
