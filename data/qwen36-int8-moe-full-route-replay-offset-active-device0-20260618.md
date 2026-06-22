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

- Mean `xpu_fused_moe`: `316.883 us`.
- Mean scratch `xpu_fused_moe`: `262.541 us`.
- Mean preallocated staged: `203.542 us`.
- Mean fused-prologue staged: `274.198 us`.
- Mean fused-prologue offset-GEMM staged: `200.269 us`.
- Mean fused-prologue active-offset-GEMM staged: `201.639 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 320.665 | 263.895 | 203.483 | 274.844 | 202.256 | 202.190 | 95.604 | 95.061 | 167.801 |
| 1 | 4 | 8 | 317.944 | 258.627 | 201.692 | 275.534 | 202.048 | 202.817 | 94.404 | 94.045 | 166.835 |
| 1 | 8 | 8 | 322.937 | 298.761 | 209.978 | 281.386 | 201.592 | 204.268 | 96.904 | 96.125 | 169.988 |
| 1 | 12 | 8 | 340.624 | 280.554 | 218.845 | 300.297 | 220.116 | 219.620 | 101.272 | 101.648 | 178.199 |
| 1 | 16 | 8 | 319.975 | 261.683 | 204.644 | 275.070 | 199.841 | 202.580 | 94.125 | 94.836 | 165.953 |
| 1 | 20 | 8 | 302.708 | 249.187 | 195.451 | 263.761 | 192.213 | 194.529 | 91.596 | 91.274 | 161.321 |
| 1 | 24 | 8 | 294.126 | 244.837 | 192.124 | 255.937 | 187.008 | 188.214 | 90.222 | 89.757 | 157.881 |
| 1 | 28 | 8 | 295.076 | 245.445 | 192.665 | 257.199 | 186.619 | 187.706 | 89.972 | 91.315 | 159.091 |
| 1 | 32 | 8 | 318.628 | 260.863 | 204.223 | 273.177 | 199.956 | 201.412 | 93.829 | 94.515 | 166.124 |
| 1 | 36 | 8 | 334.095 | 271.161 | 211.734 | 287.420 | 209.137 | 210.714 | 98.928 | 98.467 | 174.519 |
| 1 | 40 | 8 | 317.443 | 261.524 | 203.037 | 273.822 | 200.555 | 202.916 | 94.813 | 94.311 | 166.362 |
| 1 | 44 | 8 | 315.914 | 260.673 | 203.823 | 275.479 | 200.290 | 202.549 | 94.628 | 93.600 | 166.863 |
| 1 | 48 | 8 | 320.511 | 262.534 | 205.461 | 275.458 | 200.410 | 203.065 | 93.680 | 94.019 | 165.369 |
| 1 | 52 | 8 | 302.968 | 250.784 | 195.139 | 262.846 | 191.643 | 194.407 | 91.730 | 91.293 | 161.011 |
| 1 | 56 | 8 | 319.975 | 261.073 | 205.462 | 274.543 | 205.003 | 200.744 | 93.607 | 93.837 | 166.686 |
| 1 | 60 | 8 | 326.541 | 269.062 | 208.903 | 280.398 | 205.618 | 208.487 | 96.145 | 96.176 | 169.605 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `16`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_offset_gemm` at `186.619 us` (`1.581x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_active_offset_gemm | 202.190 | 1.586 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | preallocated_staged | 201.692 | 1.576 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | fused_prologue_offset_gemm | 201.592 | 1.602 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | preallocated_staged | 218.845 | 1.556 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | fused_prologue_offset_gemm | 199.841 | 1.601 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | fused_prologue_offset_gemm | 192.213 | 1.575 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | fused_prologue_offset_gemm | 187.008 | 1.573 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | fused_prologue_offset_gemm | 186.619 | 1.581 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | fused_prologue_offset_gemm | 199.956 | 1.593 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | fused_prologue_offset_gemm | 209.137 | 1.597 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | fused_prologue_offset_gemm | 200.555 | 1.583 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | fused_prologue_offset_gemm | 200.290 | 1.577 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | fused_prologue_offset_gemm | 200.410 | 1.599 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 52 | fused_prologue_offset_gemm | 191.643 | 1.581 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | fused_prologue_active_offset_gemm | 200.744 | 1.594 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | fused_prologue_offset_gemm | 205.618 | 1.588 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
