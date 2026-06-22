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

- Mean `xpu_fused_moe`: `328.451 us`.
- Mean scratch `xpu_fused_moe`: `268.705 us`.
- Mean prologue-scratch `xpu_fused_moe`: `291.040 us`.
- Mean preallocated staged: `214.895 us`.
- Mean fused-prologue staged: `289.689 us`.
- Mean fused-prologue offset-GEMM staged: `212.014 us`.
- Mean fused-prologue active-offset-GEMM staged: `213.951 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 321.168 | 268.999 | 288.701 | 208.611 | 285.557 | 206.657 | 209.410 | n/a | n/a | 96.342 | 97.032 | 167.999 |
| 1 | 40 | 8 | 334.424 | 277.305 | 296.049 | 217.808 | 292.164 | 215.262 | 217.826 | n/a | n/a | 100.719 | 99.994 | 175.222 |
| 1 | 80 | 8 | 312.610 | 253.056 | 277.019 | 206.067 | 274.535 | 202.034 | 202.872 | n/a | n/a | 94.470 | 94.543 | 163.710 |
| 1 | 85 | 8 | 331.265 | 261.434 | 284.093 | 215.541 | 291.319 | 212.739 | 215.510 | n/a | n/a | 99.122 | 98.536 | 169.928 |
| 1 | 95 | 8 | 326.927 | 267.520 | 289.605 | 214.343 | 287.593 | 210.603 | 212.622 | n/a | n/a | 97.671 | 98.648 | 168.923 |
| 1 | 100 | 8 | 329.425 | 273.242 | 298.893 | 216.414 | 293.595 | 214.154 | 215.630 | n/a | n/a | 99.440 | 99.755 | 172.002 |
| 1 | 115 | 8 | 343.334 | 279.384 | 302.920 | 225.480 | 303.058 | 222.653 | 223.791 | n/a | n/a | 103.485 | 103.844 | 177.913 |

## Graph Replay Timing

These timings capture each eligible candidate in an XPU graph and time `graph.replay()`. They remain single-device replay diagnostics, not endpoint throughput.

| rows | route start | candidate | status | graph us |
|---:|---:|---|---|---:|
| 1 | 0 | xpu_fused_moe_with_scratch | executed | 337.596 |
| 1 | 0 | xpu_fused_moe_with_prologue_scratch | executed | 233.687 |
| 1 | 0 | preallocated_staged | executed | 166.170 |
| 1 | 0 | fused_prologue_staged | executed | 178.593 |
| 1 | 0 | fused_prologue_offset_gemm | executed | 183.918 |
| 1 | 0 | fused_prologue_active_offset_gemm | executed | 155.486 |
| 1 | 40 | xpu_fused_moe_with_scratch | executed | 332.762 |
| 1 | 40 | xpu_fused_moe_with_prologue_scratch | executed | 258.321 |
| 1 | 40 | preallocated_staged | executed | 175.726 |
| 1 | 40 | fused_prologue_staged | executed | 181.824 |
| 1 | 40 | fused_prologue_offset_gemm | executed | 173.049 |
| 1 | 40 | fused_prologue_active_offset_gemm | executed | 147.622 |
| 1 | 80 | xpu_fused_moe_with_scratch | executed | 317.762 |
| 1 | 80 | xpu_fused_moe_with_prologue_scratch | executed | 308.107 |
| 1 | 80 | preallocated_staged | executed | 286.016 |
| 1 | 80 | fused_prologue_staged | executed | 179.039 |
| 1 | 80 | fused_prologue_offset_gemm | executed | 187.896 |
| 1 | 80 | fused_prologue_active_offset_gemm | executed | 155.214 |
| 1 | 85 | xpu_fused_moe_with_scratch | executed | 327.523 |
| 1 | 85 | xpu_fused_moe_with_prologue_scratch | executed | 335.786 |
| 1 | 85 | preallocated_staged | executed | 281.186 |
| 1 | 85 | fused_prologue_staged | executed | 179.083 |
| 1 | 85 | fused_prologue_offset_gemm | executed | 176.478 |
| 1 | 85 | fused_prologue_active_offset_gemm | executed | 155.564 |
| 1 | 95 | xpu_fused_moe_with_scratch | executed | 318.674 |
| 1 | 95 | xpu_fused_moe_with_prologue_scratch | executed | 307.821 |
| 1 | 95 | preallocated_staged | executed | 318.650 |
| 1 | 95 | fused_prologue_staged | executed | 180.728 |
| 1 | 95 | fused_prologue_offset_gemm | executed | 176.298 |
| 1 | 95 | fused_prologue_active_offset_gemm | executed | 175.058 |
| 1 | 100 | xpu_fused_moe_with_scratch | executed | 336.889 |
| 1 | 100 | xpu_fused_moe_with_prologue_scratch | executed | 316.802 |
| 1 | 100 | preallocated_staged | executed | 277.906 |
| 1 | 100 | fused_prologue_staged | executed | 179.332 |
| 1 | 100 | fused_prologue_offset_gemm | executed | 174.852 |
| 1 | 100 | fused_prologue_active_offset_gemm | executed | 156.629 |
| 1 | 115 | xpu_fused_moe_with_scratch | executed | 333.353 |
| 1 | 115 | xpu_fused_moe_with_prologue_scratch | executed | 334.943 |
| 1 | 115 | preallocated_staged | executed | 194.177 |
| 1 | 115 | fused_prologue_staged | executed | 177.750 |
| 1 | 115 | fused_prologue_offset_gemm | executed | 178.627 |
| 1 | 115 | fused_prologue_active_offset_gemm | executed | 161.426 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `202.034 us` (`1.547x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_offset_gemm | 206.657 | 1.554 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | fused_prologue_offset_gemm | 215.262 | 1.554 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | fused_prologue_offset_gemm | 202.034 | 1.547 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | fused_prologue_offset_gemm | 212.739 | 1.557 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | fused_prologue_offset_gemm | 210.603 | 1.552 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | fused_prologue_offset_gemm | 214.154 | 1.538 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | fused_prologue_offset_gemm | 222.653 | 1.542 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
