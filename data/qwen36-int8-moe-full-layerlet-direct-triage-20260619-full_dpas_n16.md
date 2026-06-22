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

- Mean `xpu_fused_moe`: `360.118 us`.
- Mean scratch `xpu_fused_moe`: `288.419 us`.
- Mean prologue-scratch `xpu_fused_moe`: `294.399 us`.
- Mean preallocated staged: `229.395 us`.
- Mean fused-prologue staged: `309.515 us`.
- Mean fused-prologue offset-GEMM staged: `227.321 us`.
- Mean fused-prologue active-offset-GEMM staged: `229.237 us`.
- Mean full C++ layerlet: `191.058 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 342.918 | 272.715 | 281.477 | 218.884 | 296.199 | 215.678 | 216.588 | n/a | 181.563 | 104.038 | 100.545 | 179.762 |
| 1 | 80 | 8 | 351.567 | 283.510 | 291.427 | 227.830 | 303.175 | 224.718 | 225.884 | n/a | 188.209 | 105.359 | 106.199 | 185.125 |
| 1 | 115 | 8 | 385.870 | 309.031 | 310.294 | 241.471 | 329.172 | 241.567 | 245.240 | n/a | 203.403 | 112.789 | 114.349 | 199.337 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 312.944 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 317.561 |
| 1 | 0 | preallocated_staged | executed | 320.369 |
| 1 | 0 | fused_prologue_staged | executed | 329.342 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 326.672 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 185.396 |
| 1 | 0 | full_layerlet | executed | 186.602 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 311.368 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 315.411 |
| 1 | 80 | preallocated_staged | executed | 170.919 |
| 1 | 80 | fused_prologue_staged | executed | 191.357 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 177.003 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 169.848 |
| 1 | 80 | full_layerlet | executed | 188.188 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 308.911 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 315.903 |
| 1 | 115 | preallocated_staged | executed | 321.885 |
| 1 | 115 | fused_prologue_staged | executed | 331.282 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 333.226 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 335.369 |
| 1 | 115 | full_layerlet | executed | 334.485 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `181.563 us` (`1.889x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 181.563 | 1.889 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 188.209 | 1.868 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 203.403 | 1.897 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
