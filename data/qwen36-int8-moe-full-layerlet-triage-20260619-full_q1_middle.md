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

- Mean `xpu_fused_moe`: `318.779 us`.
- Mean scratch `xpu_fused_moe`: `261.102 us`.
- Mean prologue-scratch `xpu_fused_moe`: `265.843 us`.
- Mean preallocated staged: `203.588 us`.
- Mean fused-prologue staged: `274.994 us`.
- Mean fused-prologue offset-GEMM staged: `201.071 us`.
- Mean fused-prologue active-offset-GEMM staged: `203.531 us`.
- Mean full C++ layerlet: `170.495 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 318.748 | 261.299 | 267.675 | 202.762 | 275.999 | 200.122 | 201.798 | n/a | 168.759 | 96.039 | 96.268 | 167.916 |
| 1 | 80 | 8 | 303.499 | 250.191 | 255.195 | 195.105 | 262.422 | 193.140 | 195.425 | n/a | 165.125 | 91.861 | 92.525 | 161.114 |
| 1 | 115 | 8 | 334.090 | 271.818 | 274.658 | 212.898 | 286.560 | 209.950 | 213.370 | n/a | 177.602 | 100.708 | 102.079 | 173.256 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 311.717 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 316.979 |
| 1 | 0 | preallocated_staged | executed | 312.439 |
| 1 | 0 | fused_prologue_staged | executed | 320.203 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 319.160 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 327.332 |
| 1 | 0 | full_layerlet | executed | 273.556 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 313.004 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 316.839 |
| 1 | 80 | preallocated_staged | executed | 312.328 |
| 1 | 80 | fused_prologue_staged | executed | 319.101 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 321.230 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 263.552 |
| 1 | 80 | full_layerlet | executed | 182.016 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 312.364 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 316.324 |
| 1 | 115 | preallocated_staged | executed | 313.776 |
| 1 | 115 | fused_prologue_staged | executed | 203.037 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 174.993 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 154.107 |
| 1 | 115 | full_layerlet | executed | 174.520 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `165.125 us` (`1.838x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 168.759 | 1.889 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 165.125 | 1.838 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 177.602 | 1.881 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
