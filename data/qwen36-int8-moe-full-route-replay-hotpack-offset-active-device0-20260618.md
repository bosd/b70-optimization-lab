# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `16`.
- Quant out-variant available: `True`.
- Route source: `data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Fused-prologue active-offset-GEMM max abs diff: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `333.305 us`.
- Mean scratch `xpu_fused_moe`: `273.384 us`.
- Mean preallocated staged: `212.744 us`.
- Mean fused-prologue staged: `288.826 us`.
- Mean fused-prologue offset-GEMM staged: `210.301 us`.
- Mean fused-prologue active-offset-GEMM staged: `212.599 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 319.654 | 262.267 | 203.759 | 276.628 | 200.510 | 212.053 | 96.944 | 100.369 | 171.025 |
| 1 | 4 | 8 | 318.512 | 257.473 | 202.580 | 280.485 | 206.248 | 205.147 | 99.025 | 100.360 | 176.774 |
| 1 | 8 | 8 | 373.112 | 300.444 | 239.200 | 313.985 | 232.828 | 231.403 | 109.226 | 109.463 | 198.633 |
| 1 | 12 | 8 | 297.937 | 247.444 | 189.771 | 257.573 | 186.212 | 190.268 | 92.428 | 91.227 | 162.611 |
| 1 | 16 | 8 | 330.699 | 273.114 | 210.161 | 280.429 | 202.722 | 211.129 | 99.623 | 98.072 | 174.380 |
| 1 | 20 | 8 | 377.281 | 310.745 | 237.422 | 325.523 | 244.468 | 238.501 | 109.103 | 110.131 | 191.655 |
| 1 | 24 | 8 | 307.663 | 251.474 | 198.626 | 264.732 | 193.282 | 195.922 | 97.980 | 92.921 | 164.779 |
| 1 | 28 | 8 | 384.058 | 308.043 | 243.128 | 334.053 | 243.199 | 241.526 | 111.899 | 111.788 | 195.530 |
| 1 | 32 | 8 | 352.947 | 285.943 | 219.636 | 299.151 | 215.847 | 224.274 | 106.704 | 104.477 | 184.962 |
| 1 | 36 | 8 | 333.557 | 273.647 | 215.663 | 297.135 | 212.217 | 215.647 | 100.275 | 103.088 | 176.899 |
| 1 | 40 | 8 | 299.894 | 247.258 | 192.235 | 261.076 | 192.759 | 196.747 | 92.260 | 91.395 | 161.810 |
| 1 | 44 | 8 | 322.582 | 257.795 | 200.933 | 272.919 | 199.720 | 202.412 | 96.288 | 97.197 | 169.471 |
| 1 | 48 | 8 | 335.079 | 279.602 | 215.212 | 293.776 | 211.137 | 210.820 | 101.880 | 100.485 | 178.506 |
| 1 | 52 | 8 | 336.469 | 278.957 | 214.614 | 294.311 | 212.370 | 215.355 | 101.050 | 100.847 | 177.708 |
| 1 | 56 | 8 | 345.951 | 289.285 | 225.049 | 304.372 | 219.206 | 218.906 | 104.406 | 103.863 | 182.475 |
| 1 | 60 | 8 | 297.487 | 250.650 | 195.908 | 265.067 | 192.088 | 191.466 | 90.808 | 92.045 | 161.526 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `16`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `186.212 us` (`1.600x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_offset_gemm | 200.510 | 1.594 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | preallocated_staged | 202.580 | 1.572 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | fused_prologue_active_offset_gemm | 231.403 | 1.612 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | fused_prologue_offset_gemm | 186.212 | 1.600 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | fused_prologue_offset_gemm | 202.722 | 1.631 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | preallocated_staged | 237.422 | 1.589 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | fused_prologue_offset_gemm | 193.282 | 1.592 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | fused_prologue_active_offset_gemm | 241.526 | 1.590 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | fused_prologue_offset_gemm | 215.847 | 1.635 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | fused_prologue_offset_gemm | 212.217 | 1.572 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | preallocated_staged | 192.235 | 1.560 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | fused_prologue_offset_gemm | 199.720 | 1.615 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | fused_prologue_active_offset_gemm | 210.820 | 1.589 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 52 | fused_prologue_offset_gemm | 212.370 | 1.584 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | fused_prologue_active_offset_gemm | 218.906 | 1.580 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | fused_prologue_active_offset_gemm | 191.466 | 1.554 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
