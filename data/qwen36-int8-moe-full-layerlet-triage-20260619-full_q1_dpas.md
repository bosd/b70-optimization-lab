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

- Mean `xpu_fused_moe`: `301.991 us`.
- Mean scratch `xpu_fused_moe`: `252.283 us`.
- Mean prologue-scratch `xpu_fused_moe`: `253.957 us`.
- Mean preallocated staged: `195.064 us`.
- Mean fused-prologue staged: `266.661 us`.
- Mean fused-prologue offset-GEMM staged: `192.460 us`.
- Mean fused-prologue active-offset-GEMM staged: `194.521 us`.
- Mean full C++ layerlet: `164.202 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 291.037 | 241.311 | 244.286 | 187.096 | 256.354 | 185.914 | 186.490 | n/a | 158.426 | 90.250 | 89.184 | 159.590 |
| 1 | 80 | 8 | 313.551 | 263.063 | 262.153 | 201.795 | 276.425 | 198.062 | 201.912 | n/a | 169.327 | 97.190 | 98.752 | 171.992 |
| 1 | 115 | 8 | 301.386 | 252.476 | 255.433 | 196.302 | 267.205 | 193.404 | 195.161 | n/a | 164.855 | 92.815 | 92.817 | 161.800 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 312.476 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 316.576 |
| 1 | 0 | preallocated_staged | executed | 312.660 |
| 1 | 0 | fused_prologue_staged | executed | 321.485 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 327.759 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 347.269 |
| 1 | 0 | full_layerlet | executed | 331.289 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 311.327 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 314.704 |
| 1 | 80 | preallocated_staged | executed | 311.769 |
| 1 | 80 | fused_prologue_staged | executed | 322.647 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 320.642 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 281.884 |
| 1 | 80 | full_layerlet | executed | 178.253 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 310.939 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 317.499 |
| 1 | 115 | preallocated_staged | executed | 311.940 |
| 1 | 115 | fused_prologue_staged | executed | 319.722 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 307.676 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 148.528 |
| 1 | 115 | full_layerlet | executed | 167.768 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `1` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `158.426 us` (`1.837x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 158.426 | 1.837 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 80 | full_layerlet | 169.327 | 1.852 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 164.855 | 1.828 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
