# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `24`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-firstdecode-route-fixture-routes-20260612ct.jsonl`.
- Route records matched: `120`; top-k rows loaded: `120`.
- Route start indices: `0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115`.
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

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `322.938 us`.
- Mean scratch `xpu_fused_moe`: `264.575 us`.
- Mean preallocated staged: `206.195 us`.
- Mean fused-prologue staged: `281.855 us`.
- Mean fused-prologue offset-GEMM staged: `206.953 us`.
- Mean fused-prologue active-offset-GEMM staged: `209.484 us`.
- Mean fused-prologue middle-layerlet staged: `177.334 us`.
- Mean full C++ layerlet: `171.433 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 295.462 | 245.773 | 192.494 | 259.359 | 194.171 | 190.668 | 162.458 | 159.903 | 89.993 | 91.449 | 158.832 |
| 1 | 5 | 8 | 294.483 | 243.443 | 191.493 | 256.934 | 188.195 | 189.564 | 161.774 | 158.262 | 91.128 | 89.953 | 159.278 |
| 1 | 10 | 8 | 330.654 | 276.997 | 215.812 | 293.282 | 213.760 | 214.952 | 180.745 | 175.893 | 100.012 | 99.114 | 176.651 |
| 1 | 15 | 8 | 304.864 | 258.196 | 200.217 | 267.814 | 195.175 | 200.268 | 169.641 | 163.133 | 95.637 | 94.257 | 165.565 |
| 1 | 20 | 8 | 310.419 | 258.664 | 198.238 | 276.735 | 200.781 | 203.322 | 172.619 | 168.787 | 94.586 | 94.420 | 169.993 |
| 1 | 25 | 8 | 346.816 | 284.386 | 220.792 | 296.537 | 219.402 | 223.213 | 191.935 | 184.115 | 103.324 | 104.239 | 182.960 |
| 1 | 30 | 8 | 347.606 | 272.711 | 215.277 | 302.595 | 220.002 | 224.938 | 188.682 | 181.984 | 103.225 | 102.922 | 180.241 |
| 1 | 35 | 8 | 316.188 | 246.763 | 196.581 | 278.259 | 201.970 | 205.015 | 173.678 | 166.523 | 95.737 | 96.327 | 167.703 |
| 1 | 40 | 8 | 333.389 | 268.174 | 211.673 | 290.881 | 213.697 | 217.065 | 183.182 | 176.384 | 101.981 | 99.389 | 175.547 |
| 1 | 45 | 8 | 331.900 | 271.345 | 211.728 | 286.031 | 211.257 | 218.596 | 180.480 | 174.692 | 99.187 | 99.552 | 174.335 |
| 1 | 50 | 8 | 322.561 | 261.692 | 207.419 | 281.668 | 207.681 | 210.976 | 177.469 | 169.997 | 96.177 | 97.439 | 170.319 |
| 1 | 55 | 8 | 347.622 | 290.011 | 227.732 | 306.653 | 221.253 | 226.535 | 189.907 | 182.596 | 103.787 | 104.329 | 186.340 |
| 1 | 60 | 8 | 333.713 | 258.515 | 200.358 | 286.094 | 211.163 | 214.821 | 180.802 | 173.176 | 98.353 | 98.254 | 173.339 |
| 1 | 65 | 8 | 387.213 | 317.517 | 243.641 | 330.692 | 238.586 | 245.300 | 206.898 | 200.772 | 114.416 | 114.793 | 200.495 |
| 1 | 70 | 8 | 330.666 | 263.177 | 204.734 | 292.022 | 216.880 | 216.239 | 184.787 | 176.569 | 102.177 | 102.858 | 178.951 |
| 1 | 75 | 8 | 320.540 | 266.159 | 206.894 | 278.722 | 208.794 | 208.496 | 177.343 | 169.830 | 98.219 | 98.951 | 173.439 |
| 1 | 80 | 8 | 320.043 | 263.593 | 207.152 | 279.169 | 206.395 | 209.565 | 176.571 | 172.664 | 97.751 | 99.719 | 178.596 |
| 1 | 85 | 8 | 357.817 | 297.390 | 222.454 | 314.389 | 232.281 | 232.993 | 197.557 | 189.937 | 108.803 | 107.085 | 190.991 |
| 1 | 90 | 8 | 318.831 | 263.493 | 206.086 | 278.105 | 207.275 | 207.821 | 175.933 | 169.444 | 98.301 | 99.135 | 173.872 |
| 1 | 95 | 8 | 321.500 | 257.903 | 203.646 | 279.008 | 206.483 | 206.537 | 175.810 | 168.610 | 97.718 | 96.458 | 170.201 |
| 1 | 100 | 8 | 294.358 | 244.856 | 189.342 | 255.778 | 188.469 | 190.317 | 161.765 | 157.106 | 91.257 | 90.572 | 159.517 |
| 1 | 105 | 8 | 290.160 | 248.974 | 191.079 | 254.332 | 186.976 | 192.587 | 164.346 | 158.572 | 90.395 | 92.108 | 161.604 |
| 1 | 110 | 8 | 297.698 | 243.871 | 192.071 | 259.087 | 187.521 | 187.831 | 159.881 | 158.123 | 90.074 | 92.971 | 159.333 |
| 1 | 115 | 8 | 295.996 | 246.211 | 191.760 | 260.378 | 188.710 | 190.008 | 161.753 | 157.326 | 91.936 | 90.236 | 159.669 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `6` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `157.106 us` (`1.874x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 159.903 | 1.848 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 5 | full_layerlet | 158.262 | 1.861 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 10 | full_layerlet | 175.893 | 1.880 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 163.133 | 1.869 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 168.787 | 1.839 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 25 | full_layerlet | 184.115 | 1.884 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 30 | full_layerlet | 181.984 | 1.910 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 35 | full_layerlet | 166.523 | 1.899 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 176.384 | 1.890 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 45 | full_layerlet | 174.692 | 1.900 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 169.997 | 1.897 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 55 | full_layerlet | 182.596 | 1.904 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 173.176 | 1.927 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 200.772 | 1.929 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 70 | full_layerlet | 176.569 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 75 | full_layerlet | 169.830 | 1.887 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 172.664 | 1.854 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 189.937 | 1.884 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 169.444 | 1.882 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 168.610 | 1.907 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 157.106 | 1.874 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 105 | full_layerlet | 158.572 | 1.830 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 110 | full_layerlet | 158.123 | 1.883 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 115 | full_layerlet | 157.326 | 1.881 | True | candidate_layerlet_meets_speed_and_exactness_gate |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
