# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `16`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
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
- Fused-prologue middle-layerlet max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `304.637 us`.
- Mean scratch `xpu_fused_moe`: `252.348 us`.
- Mean preallocated staged: `197.376 us`.
- Mean fused-prologue staged: `266.664 us`.
- Mean fused-prologue offset-GEMM staged: `194.617 us`.
- Mean fused-prologue active-offset-GEMM staged: `196.920 us`.
- Mean fused-prologue middle-layerlet staged: `167.315 us`.
- Mean full C++ layerlet: `161.743 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 309.599 | 257.126 | 198.562 | 270.194 | 194.816 | 198.092 | 169.244 | 162.772 | 93.591 | 93.701 | 164.533 |
| 1 | 4 | 8 | 294.336 | 244.601 | 190.996 | 257.658 | 186.800 | 188.755 | 160.838 | 156.232 | 90.648 | 89.702 | 161.566 |
| 1 | 8 | 8 | 297.582 | 243.506 | 191.102 | 258.263 | 185.827 | 188.767 | 163.849 | 157.373 | 89.989 | 89.291 | 157.064 |
| 1 | 12 | 8 | 297.771 | 247.274 | 193.639 | 259.769 | 191.039 | 192.920 | 164.518 | 159.394 | 91.021 | 90.749 | 160.708 |
| 1 | 16 | 8 | 317.552 | 260.595 | 204.747 | 276.557 | 203.291 | 205.767 | 173.867 | 166.925 | 94.664 | 95.453 | 167.844 |
| 1 | 20 | 8 | 321.840 | 264.217 | 206.159 | 280.221 | 205.584 | 212.599 | 175.821 | 171.005 | 97.089 | 96.266 | 170.300 |
| 1 | 24 | 8 | 310.809 | 259.766 | 203.051 | 274.603 | 200.661 | 203.580 | 171.090 | 165.188 | 94.375 | 95.767 | 167.449 |
| 1 | 28 | 8 | 312.532 | 260.321 | 204.098 | 276.172 | 202.885 | 203.833 | 172.567 | 165.381 | 94.768 | 95.463 | 167.144 |
| 1 | 32 | 8 | 320.010 | 265.831 | 210.943 | 282.168 | 204.547 | 208.650 | 175.377 | 168.811 | 96.505 | 96.765 | 168.740 |
| 1 | 36 | 8 | 316.507 | 261.603 | 203.838 | 275.948 | 202.729 | 204.552 | 173.384 | 167.509 | 95.508 | 95.236 | 171.161 |
| 1 | 40 | 8 | 309.215 | 255.878 | 200.824 | 270.807 | 198.552 | 199.134 | 167.820 | 164.779 | 93.792 | 94.210 | 164.545 |
| 1 | 44 | 8 | 293.323 | 243.207 | 188.497 | 256.143 | 187.264 | 188.729 | 160.084 | 155.263 | 90.638 | 89.402 | 158.004 |
| 1 | 48 | 8 | 292.822 | 243.292 | 189.136 | 255.885 | 186.989 | 188.578 | 161.198 | 156.107 | 89.736 | 89.688 | 157.768 |
| 1 | 52 | 8 | 292.862 | 242.649 | 190.252 | 256.991 | 187.436 | 188.588 | 160.370 | 156.553 | 89.409 | 88.998 | 157.891 |
| 1 | 56 | 8 | 291.041 | 243.154 | 190.667 | 256.369 | 185.969 | 188.313 | 164.327 | 156.893 | 89.192 | 88.651 | 157.801 |
| 1 | 60 | 8 | 296.398 | 244.553 | 191.507 | 258.872 | 189.483 | 189.859 | 162.692 | 157.702 | 90.407 | 89.764 | 159.598 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `8` / `16`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `155.263 us` (`1.889x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 162.772 | 1.902 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | full_layerlet | 156.232 | 1.884 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 8 | full_layerlet | 157.373 | 1.891 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 12 | full_layerlet | 159.394 | 1.868 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 16 | full_layerlet | 166.925 | 1.902 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 171.005 | 1.882 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | full_layerlet | 165.188 | 1.882 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | full_layerlet | 165.381 | 1.890 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | full_layerlet | 168.811 | 1.896 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | full_layerlet | 167.509 | 1.889 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 164.779 | 1.877 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | full_layerlet | 155.263 | 1.889 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 48 | full_layerlet | 156.107 | 1.876 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 52 | full_layerlet | 156.553 | 1.871 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 56 | full_layerlet | 156.893 | 1.855 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 60 | full_layerlet | 157.702 | 1.879 | True | candidate_layerlet_meets_speed_and_exactness_gate |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
