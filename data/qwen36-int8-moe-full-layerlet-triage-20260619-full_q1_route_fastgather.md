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

- Mean `xpu_fused_moe`: `319.722 us`.
- Mean scratch `xpu_fused_moe`: `262.548 us`.
- Mean prologue-scratch `xpu_fused_moe`: `268.114 us`.
- Mean preallocated staged: `206.303 us`.
- Mean fused-prologue staged: `279.711 us`.
- Mean fused-prologue offset-GEMM staged: `203.587 us`.
- Mean fused-prologue active-offset-GEMM staged: `205.614 us`.
- Mean full C++ layerlet: `173.146 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 335.132 | 271.236 | 278.480 | 213.864 | 293.324 | 212.949 | 215.210 | n/a | 180.662 | 100.692 | 100.501 | 174.638 |
| 1 | 80 | 8 | 307.954 | 254.893 | 259.902 | 200.907 | 269.620 | 197.470 | 197.824 | n/a | 167.028 | 93.939 | 95.632 | 164.393 |
| 1 | 115 | 8 | 316.081 | 261.514 | 265.961 | 204.140 | 276.190 | 200.342 | 203.809 | n/a | 171.750 | 97.027 | 96.074 | 167.284 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 332.745 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 332.106 |
| 1 | 0 | preallocated_staged | executed | 325.606 |
| 1 | 0 | fused_prologue_staged | executed | 332.095 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 338.179 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 184.257 |
| 1 | 0 | full_layerlet | executed | 178.347 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 310.723 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 331.222 |
| 1 | 80 | preallocated_staged | executed | 321.851 |
| 1 | 80 | fused_prologue_staged | executed | 312.569 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 173.048 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 161.463 |
| 1 | 80 | full_layerlet | executed | 167.196 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 308.220 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 317.507 |
| 1 | 115 | preallocated_staged | executed | 312.884 |
| 1 | 115 | fused_prologue_staged | executed | 171.764 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 166.806 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 144.235 |
| 1 | 115 | full_layerlet | executed | 174.054 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `167.028 us` (`1.844x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 180.662 | 1.855 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 167.028 | 1.844 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 171.750 | 1.840 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
