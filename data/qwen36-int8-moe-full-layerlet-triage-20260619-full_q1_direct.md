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

- Mean `xpu_fused_moe`: `305.729 us`.
- Mean scratch `xpu_fused_moe`: `251.825 us`.
- Mean prologue-scratch `xpu_fused_moe`: `258.039 us`.
- Mean preallocated staged: `197.914 us`.
- Mean fused-prologue staged: `267.148 us`.
- Mean fused-prologue offset-GEMM staged: `194.838 us`.
- Mean fused-prologue active-offset-GEMM staged: `196.749 us`.
- Mean full C++ layerlet: `163.259 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 314.854 | 256.749 | 262.430 | 203.469 | 274.406 | 198.756 | 200.935 | n/a | 165.582 | 95.357 | 94.361 | 167.206 |
| 1 | 80 | 8 | 306.200 | 252.934 | 260.959 | 198.715 | 267.178 | 196.283 | 197.783 | n/a | 163.694 | 93.579 | 93.871 | 163.907 |
| 1 | 115 | 8 | 296.135 | 245.790 | 250.728 | 191.558 | 259.859 | 189.476 | 191.527 | n/a | 160.501 | 92.019 | 90.634 | 158.006 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 311.919 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 317.819 |
| 1 | 0 | preallocated_staged | executed | 314.304 |
| 1 | 0 | fused_prologue_staged | executed | 325.577 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 323.812 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 315.159 |
| 1 | 0 | full_layerlet | executed | 326.134 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 310.604 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 320.442 |
| 1 | 80 | preallocated_staged | executed | 309.156 |
| 1 | 80 | fused_prologue_staged | executed | 319.241 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 318.367 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 295.672 |
| 1 | 80 | full_layerlet | executed | 176.589 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 310.016 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 316.194 |
| 1 | 115 | preallocated_staged | executed | 311.893 |
| 1 | 115 | fused_prologue_staged | executed | 320.068 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 319.114 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 219.788 |
| 1 | 115 | full_layerlet | executed | 176.868 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `160.501 us` (`1.845x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 165.582 | 1.902 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 163.694 | 1.871 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 160.501 | 1.845 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
