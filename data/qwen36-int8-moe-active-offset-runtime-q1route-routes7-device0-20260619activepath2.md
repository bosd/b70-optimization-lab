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

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `318.339 us`.
- Mean scratch `xpu_fused_moe`: `263.538 us`.
- Mean preallocated staged: `204.748 us`.
- Mean fused-prologue staged: `278.544 us`.
- Mean fused-prologue offset-GEMM staged: `204.210 us`.
- Mean fused-prologue active-offset-GEMM staged: `206.751 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 349.368 | 287.009 | 222.079 | 304.679 | 223.191 | 225.467 | n/a | n/a | 105.294 | 105.210 | 185.652 |
| 1 | 40 | 8 | 327.487 | 270.528 | 211.996 | 286.954 | 210.962 | 213.891 | n/a | n/a | 97.821 | 97.715 | 173.944 |
| 1 | 80 | 8 | 324.388 | 270.911 | 208.610 | 283.284 | 207.657 | 210.503 | n/a | n/a | 99.766 | 98.981 | 175.342 |
| 1 | 85 | 8 | 309.063 | 254.715 | 198.318 | 269.598 | 197.774 | 201.281 | n/a | n/a | 94.260 | 94.215 | 166.755 |
| 1 | 95 | 8 | 297.995 | 247.939 | 193.071 | 261.637 | 192.002 | 193.810 | n/a | n/a | 91.834 | 91.036 | 160.475 |
| 1 | 100 | 8 | 318.989 | 262.791 | 204.140 | 278.224 | 204.309 | 206.148 | n/a | n/a | 96.223 | 94.908 | 167.517 |
| 1 | 115 | 8 | 301.082 | 250.871 | 195.025 | 265.434 | 193.578 | 196.155 | n/a | n/a | 92.295 | 92.327 | 161.125 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 328.191 |
| 1 | 0 | preallocated_staged | executed | 338.837 |
| 1 | 0 | fused_prologue_staged | executed | 229.813 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 186.950 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 173.529 |
| 1 | 40 | xpu_fused_moe_with_scratch | executed | 317.860 |
| 1 | 40 | preallocated_staged | executed | 317.721 |
| 1 | 40 | fused_prologue_staged | executed | 337.383 |
| 1 | 40 | fused_prologue_offset_gemm | executed | 335.076 |
| 1 | 40 | fused_prologue_active_offset_gemm | executed | 329.729 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 321.553 |
| 1 | 80 | preallocated_staged | executed | 330.244 |
| 1 | 80 | fused_prologue_staged | executed | 195.571 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 180.493 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 162.764 |
| 1 | 85 | xpu_fused_moe_with_scratch | executed | 320.330 |
| 1 | 85 | preallocated_staged | executed | 219.447 |
| 1 | 85 | fused_prologue_staged | executed | 182.612 |
| 1 | 85 | fused_prologue_offset_gemm | executed | 177.405 |
| 1 | 85 | fused_prologue_active_offset_gemm | executed | 160.129 |
| 1 | 95 | xpu_fused_moe_with_scratch | executed | 319.481 |
| 1 | 95 | preallocated_staged | executed | 201.470 |
| 1 | 95 | fused_prologue_staged | executed | 181.068 |
| 1 | 95 | fused_prologue_offset_gemm | executed | 175.588 |
| 1 | 95 | fused_prologue_active_offset_gemm | executed | 155.019 |
| 1 | 100 | xpu_fused_moe_with_scratch | executed | 318.144 |
| 1 | 100 | preallocated_staged | executed | 319.279 |
| 1 | 100 | fused_prologue_staged | executed | 325.842 |
| 1 | 100 | fused_prologue_offset_gemm | executed | 324.397 |
| 1 | 100 | fused_prologue_active_offset_gemm | executed | 310.742 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 320.023 |
| 1 | 115 | preallocated_staged | executed | 327.401 |
| 1 | 115 | fused_prologue_staged | executed | 336.569 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 247.305 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 149.183 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `192.002 us` (`1.552x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | preallocated_staged | 222.079 | 1.573 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | fused_prologue_offset_gemm | 210.962 | 1.552 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | fused_prologue_offset_gemm | 207.657 | 1.562 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | fused_prologue_offset_gemm | 197.774 | 1.563 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | fused_prologue_offset_gemm | 192.002 | 1.552 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | preallocated_staged | 204.140 | 1.563 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | fused_prologue_offset_gemm | 193.578 | 1.555 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
