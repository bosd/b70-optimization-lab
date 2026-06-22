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

- Mean `xpu_fused_moe`: `333.633 us`.
- Mean scratch `xpu_fused_moe`: `276.105 us`.
- Mean prologue-scratch `xpu_fused_moe`: `281.698 us`.
- Mean preallocated staged: `216.717 us`.
- Mean fused-prologue staged: `288.482 us`.
- Mean fused-prologue offset-GEMM staged: `212.965 us`.
- Mean fused-prologue active-offset-GEMM staged: `215.204 us`.
- Mean full C++ layerlet: `178.276 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 340.418 | 279.301 | 280.897 | 215.560 | 291.606 | 214.313 | 217.896 | n/a | 180.476 | 102.858 | 102.182 | 177.932 |
| 1 | 80 | 8 | 311.480 | 261.399 | 270.013 | 210.919 | 272.770 | 199.884 | 202.127 | n/a | 168.178 | 95.313 | 95.146 | 166.547 |
| 1 | 115 | 8 | 349.000 | 287.615 | 294.183 | 223.673 | 301.070 | 224.697 | 225.588 | n/a | 186.172 | 104.621 | 107.577 | 184.705 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 312.907 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 319.761 |
| 1 | 0 | preallocated_staged | executed | 314.925 |
| 1 | 0 | fused_prologue_staged | executed | 317.944 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 314.561 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 229.616 |
| 1 | 0 | full_layerlet | executed | 167.630 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 314.150 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 316.732 |
| 1 | 80 | preallocated_staged | executed | 328.502 |
| 1 | 80 | fused_prologue_staged | executed | 328.744 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 195.283 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 181.818 |
| 1 | 80 | full_layerlet | executed | 178.027 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 329.654 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 327.777 |
| 1 | 115 | preallocated_staged | executed | 327.556 |
| 1 | 115 | fused_prologue_staged | executed | 329.277 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 337.077 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 328.856 |
| 1 | 115 | full_layerlet | executed | 329.722 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `168.178 us` (`1.852x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 180.476 | 1.886 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 168.178 | 1.852 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 186.172 | 1.875 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
