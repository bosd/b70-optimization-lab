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

- Mean `xpu_fused_moe`: `316.980 us`.
- Mean scratch `xpu_fused_moe`: `264.523 us`.
- Mean prologue-scratch `xpu_fused_moe`: `266.441 us`.
- Mean preallocated staged: `205.201 us`.
- Mean fused-prologue staged: `278.262 us`.
- Mean fused-prologue offset-GEMM staged: `202.260 us`.
- Mean fused-prologue active-offset-GEMM staged: `204.286 us`.
- Mean full C++ layerlet: `171.748 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 330.532 | 276.868 | 277.828 | 213.578 | 291.982 | 212.314 | 212.053 | n/a | 177.308 | 100.443 | 101.337 | 175.340 |
| 1 | 80 | 8 | 308.212 | 259.668 | 261.404 | 200.162 | 270.598 | 196.875 | 200.063 | n/a | 168.217 | 94.118 | 98.031 | 168.161 |
| 1 | 115 | 8 | 312.197 | 257.033 | 260.092 | 201.863 | 272.206 | 197.591 | 200.743 | n/a | 169.721 | 95.720 | 96.767 | 165.302 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 313.479 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 317.130 |
| 1 | 0 | preallocated_staged | executed | 313.373 |
| 1 | 0 | fused_prologue_staged | executed | 321.196 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 319.324 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 318.313 |
| 1 | 0 | full_layerlet | executed | 190.479 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 314.795 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 318.518 |
| 1 | 80 | preallocated_staged | executed | 313.838 |
| 1 | 80 | fused_prologue_staged | executed | 323.066 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 180.487 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 147.001 |
| 1 | 80 | full_layerlet | executed | 168.571 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 311.737 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 316.423 |
| 1 | 115 | preallocated_staged | executed | 312.153 |
| 1 | 115 | fused_prologue_staged | executed | 227.396 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 177.395 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 154.167 |
| 1 | 115 | full_layerlet | executed | 178.591 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `168.217 us` (`1.832x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 177.308 | 1.864 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 168.217 | 1.832 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 169.721 | 1.839 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
