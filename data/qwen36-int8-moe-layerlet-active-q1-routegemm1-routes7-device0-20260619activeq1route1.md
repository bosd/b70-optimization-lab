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

- Mean `xpu_fused_moe`: `322.860 us`.
- Mean scratch `xpu_fused_moe`: `268.111 us`.
- Mean preallocated staged: `208.546 us`.
- Mean fused-prologue staged: `282.273 us`.
- Mean fused-prologue offset-GEMM staged: `207.278 us`.
- Mean fused-prologue active-offset-GEMM staged: `208.230 us`.
- Mean full C++ layerlet: `173.508 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 319.546 | 266.349 | 206.027 | 280.363 | 211.526 | 206.082 | n/a | 173.281 | 99.187 | 97.908 | 171.993 |
| 1 | 40 | 8 | 309.938 | 258.712 | 201.793 | 271.168 | 198.586 | 200.731 | n/a | 167.267 | 95.031 | 95.863 | 167.893 |
| 1 | 80 | 8 | 329.709 | 269.715 | 211.057 | 286.343 | 209.017 | 210.909 | n/a | 175.766 | 98.381 | 99.178 | 173.153 |
| 1 | 85 | 8 | 308.937 | 255.806 | 199.467 | 268.924 | 197.660 | 199.455 | n/a | 166.501 | 95.312 | 95.551 | 165.359 |
| 1 | 95 | 8 | 318.857 | 263.624 | 205.455 | 279.078 | 203.957 | 206.352 | n/a | 171.523 | 96.433 | 96.470 | 168.601 |
| 1 | 100 | 8 | 327.040 | 273.004 | 211.677 | 285.369 | 208.936 | 211.244 | n/a | 174.583 | 99.585 | 100.152 | 173.198 |
| 1 | 115 | 8 | 345.993 | 289.569 | 224.345 | 304.666 | 221.264 | 222.839 | n/a | 185.634 | 106.889 | 107.494 | 184.594 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 317.894 |
| 1 | 0 | preallocated_staged | executed | 219.154 |
| 1 | 0 | fused_prologue_staged | executed | 179.584 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 174.451 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 159.482 |
| 1 | 0 | full_layerlet | executed | 177.641 |
| 1 | 40 | xpu_fused_moe_with_scratch | executed | 319.094 |
| 1 | 40 | preallocated_staged | executed | 344.183 |
| 1 | 40 | fused_prologue_staged | executed | 304.027 |
| 1 | 40 | fused_prologue_offset_gemm | executed | 180.412 |
| 1 | 40 | fused_prologue_active_offset_gemm | executed | 158.328 |
| 1 | 40 | full_layerlet | executed | 180.435 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 318.297 |
| 1 | 80 | preallocated_staged | executed | 328.993 |
| 1 | 80 | fused_prologue_staged | executed | 325.214 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 174.798 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 158.088 |
| 1 | 80 | full_layerlet | executed | 174.496 |
| 1 | 85 | xpu_fused_moe_with_scratch | executed | 321.315 |
| 1 | 85 | preallocated_staged | executed | 321.275 |
| 1 | 85 | fused_prologue_staged | executed | 328.136 |
| 1 | 85 | fused_prologue_offset_gemm | executed | 325.212 |
| 1 | 85 | fused_prologue_active_offset_gemm | executed | 156.618 |
| 1 | 85 | full_layerlet | executed | 176.054 |
| 1 | 95 | xpu_fused_moe_with_scratch | executed | 318.051 |
| 1 | 95 | preallocated_staged | executed | 317.783 |
| 1 | 95 | fused_prologue_staged | executed | 325.566 |
| 1 | 95 | fused_prologue_offset_gemm | executed | 323.380 |
| 1 | 95 | fused_prologue_active_offset_gemm | executed | 230.339 |
| 1 | 95 | full_layerlet | executed | 178.244 |
| 1 | 100 | xpu_fused_moe_with_scratch | executed | 317.403 |
| 1 | 100 | preallocated_staged | executed | 326.084 |
| 1 | 100 | fused_prologue_staged | executed | 335.251 |
| 1 | 100 | fused_prologue_offset_gemm | executed | 335.416 |
| 1 | 100 | fused_prologue_active_offset_gemm | executed | 221.616 |
| 1 | 100 | full_layerlet | executed | 180.467 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 326.486 |
| 1 | 115 | preallocated_staged | executed | 338.802 |
| 1 | 115 | fused_prologue_staged | executed | 334.161 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 189.123 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 177.185 |
| 1 | 115 | full_layerlet | executed | 170.024 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `166.501 us` (`1.855x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 173.281 | 1.844 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 167.267 | 1.853 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 175.766 | 1.876 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 166.501 | 1.855 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 171.523 | 1.859 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 174.583 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 185.634 | 1.864 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
