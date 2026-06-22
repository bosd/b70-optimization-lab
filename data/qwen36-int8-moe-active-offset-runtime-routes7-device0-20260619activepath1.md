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

- Mean `xpu_fused_moe`: `321.353 us`.
- Mean scratch `xpu_fused_moe`: `266.200 us`.
- Mean preallocated staged: `208.506 us`.
- Mean fused-prologue staged: `283.045 us`.
- Mean fused-prologue offset-GEMM staged: `206.445 us`.
- Mean fused-prologue active-offset-GEMM staged: `208.761 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 359.974 | 296.633 | 232.939 | 319.204 | 230.129 | 231.861 | n/a | n/a | 111.170 | 109.524 | 190.621 |
| 1 | 40 | 8 | 309.992 | 256.791 | 200.653 | 270.679 | 198.365 | 201.936 | n/a | n/a | 96.351 | 95.977 | 168.101 |
| 1 | 80 | 8 | 302.288 | 251.659 | 197.423 | 266.573 | 195.775 | 196.786 | n/a | n/a | 94.143 | 94.891 | 164.017 |
| 1 | 85 | 8 | 306.481 | 254.048 | 199.333 | 270.056 | 197.423 | 199.582 | n/a | n/a | 95.052 | 94.805 | 166.869 |
| 1 | 95 | 8 | 307.164 | 254.472 | 199.513 | 269.697 | 197.622 | 200.317 | n/a | n/a | 94.948 | 95.117 | 167.683 |
| 1 | 100 | 8 | 351.981 | 290.359 | 226.045 | 310.740 | 225.651 | 228.565 | n/a | n/a | 107.843 | 108.806 | 186.250 |
| 1 | 115 | 8 | 311.591 | 259.439 | 203.635 | 274.364 | 200.146 | 202.283 | n/a | n/a | 97.683 | 97.544 | 168.937 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 333.407 |
| 1 | 0 | preallocated_staged | executed | 301.281 |
| 1 | 0 | fused_prologue_staged | executed | 195.972 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 191.758 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 182.719 |
| 1 | 40 | xpu_fused_moe_with_scratch | executed | 321.328 |
| 1 | 40 | preallocated_staged | executed | 330.318 |
| 1 | 40 | fused_prologue_staged | executed | 340.854 |
| 1 | 40 | fused_prologue_offset_gemm | executed | 338.565 |
| 1 | 40 | fused_prologue_active_offset_gemm | executed | 279.866 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 323.281 |
| 1 | 80 | preallocated_staged | executed | 330.043 |
| 1 | 80 | fused_prologue_staged | executed | 324.569 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 176.823 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 158.926 |
| 1 | 85 | xpu_fused_moe_with_scratch | executed | 319.442 |
| 1 | 85 | preallocated_staged | executed | 307.987 |
| 1 | 85 | fused_prologue_staged | executed | 179.948 |
| 1 | 85 | fused_prologue_offset_gemm | executed | 175.948 |
| 1 | 85 | fused_prologue_active_offset_gemm | executed | 158.536 |
| 1 | 95 | xpu_fused_moe_with_scratch | executed | 318.675 |
| 1 | 95 | preallocated_staged | executed | 202.005 |
| 1 | 95 | fused_prologue_staged | executed | 180.940 |
| 1 | 95 | fused_prologue_offset_gemm | executed | 181.433 |
| 1 | 95 | fused_prologue_active_offset_gemm | executed | 157.464 |
| 1 | 100 | xpu_fused_moe_with_scratch | executed | 332.673 |
| 1 | 100 | preallocated_staged | executed | 337.873 |
| 1 | 100 | fused_prologue_staged | executed | 338.100 |
| 1 | 100 | fused_prologue_offset_gemm | executed | 219.946 |
| 1 | 100 | fused_prologue_active_offset_gemm | executed | 150.339 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 339.192 |
| 1 | 115 | preallocated_staged | executed | 267.448 |
| 1 | 115 | fused_prologue_staged | executed | 191.169 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 184.772 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 161.308 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `195.775 us` (`1.544x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_offset_gemm | 230.129 | 1.564 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | fused_prologue_offset_gemm | 198.365 | 1.563 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | fused_prologue_offset_gemm | 195.775 | 1.544 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | fused_prologue_offset_gemm | 197.423 | 1.552 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | fused_prologue_offset_gemm | 197.622 | 1.554 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | fused_prologue_offset_gemm | 225.651 | 1.560 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | fused_prologue_offset_gemm | 200.146 | 1.557 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
