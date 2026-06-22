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

- Mean `xpu_fused_moe`: `337.195 us`.
- Mean scratch `xpu_fused_moe`: `270.146 us`.
- Mean prologue-scratch `xpu_fused_moe`: `278.864 us`.
- Mean preallocated staged: `218.424 us`.
- Mean fused-prologue staged: `292.473 us`.
- Mean fused-prologue offset-GEMM staged: `214.421 us`.
- Mean fused-prologue active-offset-GEMM staged: `215.731 us`.
- Mean full C++ layerlet: `178.647 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 344.562 | 269.684 | 281.020 | 221.466 | 298.116 | 216.791 | 217.920 | n/a | 181.281 | 102.757 | 104.908 | 179.374 |
| 1 | 80 | 8 | 328.428 | 267.800 | 271.659 | 209.978 | 281.088 | 207.721 | 209.992 | n/a | 173.620 | 97.954 | 99.470 | 172.266 |
| 1 | 115 | 8 | 338.595 | 272.954 | 283.911 | 223.828 | 298.214 | 218.750 | 219.281 | n/a | 181.041 | 102.701 | 101.649 | 178.239 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 325.796 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 327.883 |
| 1 | 0 | preallocated_staged | executed | 331.412 |
| 1 | 0 | fused_prologue_staged | executed | 330.281 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 331.193 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 201.362 |
| 1 | 0 | full_layerlet | executed | 193.536 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 314.319 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 319.670 |
| 1 | 80 | preallocated_staged | executed | 273.746 |
| 1 | 80 | fused_prologue_staged | executed | 172.786 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 168.698 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 146.838 |
| 1 | 80 | full_layerlet | executed | 168.373 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 310.391 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 317.213 |
| 1 | 115 | preallocated_staged | executed | 312.130 |
| 1 | 115 | fused_prologue_staged | executed | 324.912 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 329.826 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 330.993 |
| 1 | 115 | full_layerlet | executed | 335.088 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `173.620 us` (`1.892x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 181.281 | 1.901 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 173.620 | 1.892 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 181.041 | 1.870 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
