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

- Mean `xpu_fused_moe`: `303.564 us`.
- Mean scratch `xpu_fused_moe`: `251.502 us`.
- Mean preallocated staged: `194.119 us`.
- Mean fused-prologue staged: `264.857 us`.
- Mean fused-prologue offset-GEMM staged: `193.954 us`.
- Mean fused-prologue active-offset-GEMM staged: `194.677 us`.
- Mean fused-prologue middle-layerlet staged: `165.064 us`.
- Mean full C++ layerlet: `160.819 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 295.830 | 247.695 | 192.225 | 260.577 | 191.417 | 193.073 | 162.954 | 158.314 | 91.915 | 91.983 | 163.079 |
| 1 | 4 | 8 | 294.188 | 246.199 | 190.875 | 259.194 | 188.448 | 188.845 | 160.066 | 172.377 | 91.971 | 90.591 | 159.338 |
| 1 | 8 | 8 | 308.117 | 255.077 | 196.609 | 265.867 | 194.064 | 193.906 | 166.026 | 160.344 | 93.843 | 93.392 | 165.643 |
| 1 | 12 | 8 | 300.964 | 249.780 | 192.922 | 262.149 | 192.464 | 192.960 | 164.471 | 159.201 | 92.156 | 91.979 | 163.133 |
| 1 | 16 | 8 | 308.462 | 255.018 | 196.453 | 268.226 | 196.007 | 197.337 | 167.119 | 160.651 | 94.467 | 100.623 | 166.270 |
| 1 | 20 | 8 | 306.455 | 253.261 | 194.967 | 267.559 | 195.829 | 196.563 | 165.691 | 159.130 | 93.777 | 93.506 | 165.084 |
| 1 | 24 | 8 | 301.047 | 249.997 | 192.429 | 262.948 | 193.676 | 195.832 | 165.665 | 159.175 | 92.869 | 99.270 | 164.258 |
| 1 | 28 | 8 | 304.252 | 251.879 | 192.953 | 264.188 | 194.477 | 194.024 | 164.854 | 159.387 | 93.404 | 92.336 | 163.096 |
| 1 | 32 | 8 | 303.834 | 248.964 | 194.690 | 261.997 | 192.050 | 192.511 | 164.384 | 161.247 | 92.605 | 92.329 | 163.348 |
| 1 | 36 | 8 | 290.051 | 241.095 | 186.231 | 253.855 | 184.753 | 185.493 | 158.506 | 154.931 | 89.235 | 89.008 | 156.933 |
| 1 | 40 | 8 | 288.550 | 241.003 | 185.839 | 253.954 | 184.070 | 184.940 | 158.127 | 154.587 | 89.875 | 89.627 | 157.657 |
| 1 | 44 | 8 | 301.763 | 252.035 | 194.002 | 265.105 | 194.636 | 194.789 | 164.126 | 159.598 | 92.993 | 92.466 | 161.978 |
| 1 | 48 | 8 | 306.725 | 251.857 | 194.010 | 266.665 | 196.255 | 197.300 | 165.644 | 159.614 | 93.454 | 93.012 | 167.411 |
| 1 | 52 | 8 | 301.685 | 248.947 | 191.818 | 261.929 | 192.157 | 192.601 | 162.807 | 157.855 | 92.609 | 91.759 | 163.147 |
| 1 | 56 | 8 | 300.505 | 251.633 | 192.423 | 265.711 | 193.676 | 194.730 | 164.937 | 158.416 | 93.340 | 91.761 | 164.325 |
| 1 | 60 | 8 | 344.594 | 279.594 | 217.455 | 297.780 | 219.284 | 219.922 | 185.650 | 178.277 | 103.482 | 102.333 | 180.697 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `11` / `16`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `154.587 us` (`1.867x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 158.314 | 1.869 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 4 | fused_prologue_middle_layerlet | 160.066 | 1.838 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | full_layerlet | 160.344 | 1.922 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | full_layerlet | 159.201 | 1.890 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 16 | full_layerlet | 160.651 | 1.920 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 159.130 | 1.926 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 24 | full_layerlet | 159.175 | 1.891 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 28 | full_layerlet | 159.387 | 1.909 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 32 | full_layerlet | 161.247 | 1.884 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | full_layerlet | 154.931 | 1.872 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 40 | full_layerlet | 154.587 | 1.867 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 44 | full_layerlet | 159.598 | 1.891 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 48 | full_layerlet | 159.614 | 1.922 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 52 | full_layerlet | 157.855 | 1.911 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 56 | full_layerlet | 158.416 | 1.897 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 60 | full_layerlet | 178.277 | 1.933 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
