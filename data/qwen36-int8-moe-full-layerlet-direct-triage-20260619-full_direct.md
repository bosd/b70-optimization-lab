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

- Mean `xpu_fused_moe`: `346.319 us`.
- Mean scratch `xpu_fused_moe`: `276.886 us`.
- Mean prologue-scratch `xpu_fused_moe`: `285.149 us`.
- Mean preallocated staged: `222.229 us`.
- Mean fused-prologue staged: `302.854 us`.
- Mean fused-prologue offset-GEMM staged: `218.434 us`.
- Mean fused-prologue active-offset-GEMM staged: `221.785 us`.
- Mean full C++ layerlet: `186.410 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 368.916 | 293.880 | 303.115 | 235.226 | 320.221 | 228.359 | 235.029 | n/a | 196.023 | 107.560 | 106.907 | 189.846 |
| 1 | 80 | 8 | 323.003 | 256.699 | 267.572 | 210.127 | 285.540 | 207.192 | 209.046 | n/a | 174.234 | 97.244 | 96.738 | 169.700 |
| 1 | 115 | 8 | 347.039 | 280.079 | 284.760 | 221.335 | 302.799 | 219.750 | 221.280 | n/a | 188.971 | 102.905 | 103.944 | 181.901 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 315.383 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 317.868 |
| 1 | 0 | preallocated_staged | executed | 314.512 |
| 1 | 0 | fused_prologue_staged | executed | 319.090 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 203.125 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 151.736 |
| 1 | 0 | full_layerlet | executed | 170.456 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 312.382 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 322.811 |
| 1 | 80 | preallocated_staged | executed | 294.822 |
| 1 | 80 | fused_prologue_staged | executed | 182.770 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 171.618 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 147.984 |
| 1 | 80 | full_layerlet | executed | 170.765 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 311.545 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 317.840 |
| 1 | 115 | preallocated_staged | executed | 311.618 |
| 1 | 115 | fused_prologue_staged | executed | 319.709 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 318.024 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 310.786 |
| 1 | 115 | full_layerlet | executed | 322.923 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `174.234 us` (`1.854x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 196.023 | 1.882 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 174.234 | 1.854 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 188.971 | 1.836 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
