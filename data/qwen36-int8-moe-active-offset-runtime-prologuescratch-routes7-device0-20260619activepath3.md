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
- Prologue-scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Fused-prologue active-offset-GEMM max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `311.790 us`.
- Mean scratch `xpu_fused_moe`: `259.909 us`.
- Mean prologue-scratch `xpu_fused_moe`: `280.209 us`.
- Mean preallocated staged: `205.599 us`.
- Mean fused-prologue staged: `275.019 us`.
- Mean fused-prologue offset-GEMM staged: `202.383 us`.
- Mean fused-prologue active-offset-GEMM staged: `203.932 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 327.182 | 275.760 | 295.888 | 217.560 | 291.748 | 213.686 | 215.063 | n/a | n/a | 101.830 | 100.825 | 176.309 |
| 1 | 40 | 8 | 316.749 | 268.596 | 288.310 | 211.116 | 281.937 | 207.714 | 210.526 | n/a | n/a | 99.038 | 97.918 | 173.080 |
| 1 | 80 | 8 | 314.020 | 261.247 | 281.482 | 204.546 | 275.415 | 202.718 | 202.592 | n/a | n/a | 98.288 | 97.860 | 169.543 |
| 1 | 85 | 8 | 310.931 | 263.215 | 280.530 | 204.774 | 274.022 | 201.502 | 203.657 | n/a | n/a | 95.865 | 96.851 | 167.296 |
| 1 | 95 | 8 | 303.791 | 253.751 | 274.592 | 199.378 | 266.797 | 195.164 | 197.012 | n/a | n/a | 93.179 | 93.853 | 163.056 |
| 1 | 100 | 8 | 303.905 | 243.652 | 265.242 | 200.324 | 266.523 | 197.061 | 198.649 | n/a | n/a | 94.073 | 93.636 | 163.923 |
| 1 | 115 | 8 | 305.949 | 253.141 | 275.416 | 201.493 | 268.692 | 198.834 | 200.022 | n/a | n/a | 94.690 | 94.725 | 165.179 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 320.621 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 167.229 |
| 1 | 0 | preallocated_staged | executed | 169.084 |
| 1 | 0 | fused_prologue_staged | executed | 181.424 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 179.826 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 155.754 |
| 1 | 40 | xpu_fused_moe_with_scratch | executed | 316.204 |
| 1 | 40 | xpu_fused_moe_with_prologue_scratch | executed | 294.259 |
| 1 | 40 | preallocated_staged | executed | 180.745 |
| 1 | 40 | fused_prologue_staged | executed | 202.826 |
| 1 | 40 | fused_prologue_offset_gemm | executed | 186.456 |
| 1 | 40 | fused_prologue_active_offset_gemm | executed | 176.105 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 321.001 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 322.819 |
| 1 | 80 | preallocated_staged | executed | 181.868 |
| 1 | 80 | fused_prologue_staged | executed | 173.211 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 180.057 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 147.736 |
| 1 | 85 | xpu_fused_moe_with_scratch | executed | 320.654 |
| 1 | 85 | xpu_fused_moe_with_prologue_scratch | executed | 314.528 |
| 1 | 85 | preallocated_staged | executed | 308.644 |
| 1 | 85 | fused_prologue_staged | executed | 188.866 |
| 1 | 85 | fused_prologue_offset_gemm | executed | 177.057 |
| 1 | 85 | fused_prologue_active_offset_gemm | executed | 158.932 |
| 1 | 95 | xpu_fused_moe_with_scratch | executed | 318.956 |
| 1 | 95 | xpu_fused_moe_with_prologue_scratch | executed | 306.394 |
| 1 | 95 | preallocated_staged | executed | 318.593 |
| 1 | 95 | fused_prologue_staged | executed | 262.065 |
| 1 | 95 | fused_prologue_offset_gemm | executed | 174.780 |
| 1 | 95 | fused_prologue_active_offset_gemm | executed | 157.995 |
| 1 | 100 | xpu_fused_moe_with_scratch | executed | 320.649 |
| 1 | 100 | xpu_fused_moe_with_prologue_scratch | executed | 319.901 |
| 1 | 100 | preallocated_staged | executed | 329.756 |
| 1 | 100 | fused_prologue_staged | executed | 335.720 |
| 1 | 100 | fused_prologue_offset_gemm | executed | 189.910 |
| 1 | 100 | fused_prologue_active_offset_gemm | executed | 147.792 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 318.754 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 312.424 |
| 1 | 115 | preallocated_staged | executed | 325.494 |
| 1 | 115 | fused_prologue_staged | executed | 327.486 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 212.751 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 155.721 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `195.164 us` (`1.557x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_offset_gemm | 213.686 | 1.531 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | fused_prologue_offset_gemm | 207.714 | 1.525 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | fused_prologue_active_offset_gemm | 202.592 | 1.550 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | fused_prologue_offset_gemm | 201.502 | 1.543 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | fused_prologue_offset_gemm | 195.164 | 1.557 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | fused_prologue_offset_gemm | 197.061 | 1.542 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | fused_prologue_offset_gemm | 198.834 | 1.539 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
