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

- Mean `xpu_fused_moe`: `319.863 us`.
- Mean scratch `xpu_fused_moe`: `262.172 us`.
- Mean preallocated staged: `203.473 us`.
- Mean fused-prologue staged: `275.990 us`.
- Mean fused-prologue offset-GEMM staged: `203.627 us`.
- Mean fused-prologue active-offset-GEMM staged: `205.816 us`.
- Mean fused-prologue middle-layerlet staged: `171.930 us`.
- Mean full C++ layerlet: `169.738 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 360.776 | 287.413 | 225.125 | 295.481 | 221.416 | 233.402 | 197.808 | 228.800 | 105.326 | 105.690 | 184.825 |
| 1 | 5 | 8 | 361.859 | 297.856 | 227.101 | 304.633 | 227.491 | 229.667 | 192.669 | 187.746 | 104.884 | 103.627 | 183.144 |
| 1 | 10 | 8 | 348.799 | 281.450 | 219.076 | 299.962 | 217.065 | 216.043 | 181.480 | 173.801 | 102.587 | 101.929 | 180.977 |
| 1 | 15 | 8 | 322.071 | 261.959 | 204.897 | 271.336 | 206.579 | 211.189 | 174.304 | 173.611 | 95.368 | 94.189 | 169.511 |
| 1 | 20 | 8 | 437.225 | 350.029 | 269.091 | 371.193 | 279.370 | 277.099 | 227.656 | 224.033 | 126.880 | 122.625 | 222.395 |
| 1 | 25 | 8 | 298.731 | 251.186 | 189.419 | 264.931 | 192.053 | 195.494 | 164.069 | 156.399 | 94.458 | 92.811 | 165.499 |
| 1 | 30 | 8 | 299.667 | 246.965 | 190.493 | 260.728 | 191.221 | 201.699 | 164.285 | 159.571 | 90.948 | 92.473 | 161.243 |
| 1 | 35 | 8 | 318.734 | 246.627 | 193.397 | 260.130 | 188.223 | 190.112 | 161.703 | 160.905 | 91.017 | 90.454 | 160.437 |
| 1 | 40 | 8 | 297.275 | 247.546 | 191.767 | 264.637 | 189.713 | 194.749 | 162.743 | 159.961 | 91.009 | 91.728 | 159.761 |
| 1 | 45 | 8 | 304.486 | 250.874 | 198.371 | 266.535 | 193.050 | 194.454 | 164.415 | 163.739 | 98.063 | 94.501 | 167.024 |
| 1 | 50 | 8 | 299.832 | 249.167 | 190.753 | 261.317 | 192.877 | 191.083 | 160.221 | 156.936 | 93.652 | 90.844 | 162.335 |
| 1 | 55 | 8 | 310.795 | 254.020 | 196.499 | 268.034 | 197.331 | 201.049 | 165.863 | 161.339 | 95.065 | 94.207 | 168.133 |
| 1 | 60 | 8 | 318.673 | 261.959 | 204.256 | 272.029 | 202.375 | 204.577 | 169.494 | 165.932 | 96.989 | 96.824 | 168.723 |
| 1 | 65 | 8 | 300.551 | 245.683 | 190.511 | 260.425 | 204.611 | 192.105 | 161.581 | 159.016 | 93.739 | 91.147 | 160.827 |
| 1 | 70 | 8 | 300.716 | 241.895 | 191.949 | 263.250 | 187.720 | 190.485 | 159.900 | 168.775 | 90.584 | 90.029 | 158.825 |
| 1 | 75 | 8 | 300.413 | 250.753 | 196.820 | 264.056 | 191.039 | 194.523 | 165.412 | 164.017 | 91.052 | 91.771 | 162.517 |
| 1 | 80 | 8 | 316.793 | 258.847 | 199.611 | 272.471 | 211.163 | 203.823 | 172.597 | 162.457 | 96.963 | 95.082 | 166.279 |
| 1 | 85 | 8 | 308.507 | 259.705 | 198.224 | 270.495 | 199.420 | 204.195 | 166.357 | 161.989 | 95.368 | 95.455 | 169.182 |
| 1 | 90 | 8 | 310.041 | 260.182 | 201.803 | 276.692 | 201.483 | 203.736 | 166.825 | 164.892 | 94.848 | 94.614 | 169.555 |
| 1 | 95 | 8 | 315.155 | 257.279 | 202.315 | 274.889 | 199.931 | 203.658 | 171.063 | 167.024 | 95.801 | 95.325 | 166.322 |
| 1 | 100 | 8 | 307.623 | 259.515 | 202.765 | 271.137 | 200.469 | 202.991 | 171.557 | 161.113 | 98.783 | 95.836 | 166.755 |
| 1 | 105 | 8 | 317.720 | 261.803 | 200.989 | 271.475 | 199.897 | 203.623 | 166.989 | 165.689 | 94.449 | 93.903 | 168.593 |
| 1 | 110 | 8 | 314.548 | 254.817 | 201.708 | 273.737 | 199.056 | 204.143 | 170.101 | 163.627 | 94.042 | 93.999 | 171.678 |
| 1 | 115 | 8 | 305.717 | 254.592 | 196.421 | 264.186 | 193.501 | 195.685 | 167.232 | 162.344 | 92.491 | 93.314 | 162.925 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `6` / `24`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `156.399 us` (`1.910x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_middle_layerlet | 197.808 | 1.824 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 5 | full_layerlet | 187.746 | 1.927 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 10 | full_layerlet | 173.801 | 2.007 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 15 | full_layerlet | 173.611 | 1.855 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 224.033 | 1.952 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 25 | full_layerlet | 156.399 | 1.910 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 30 | full_layerlet | 159.571 | 1.878 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 35 | full_layerlet | 160.905 | 1.981 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 159.961 | 1.858 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 45 | full_layerlet | 163.739 | 1.860 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 50 | full_layerlet | 156.936 | 1.911 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 55 | full_layerlet | 161.339 | 1.926 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 165.932 | 1.921 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 65 | full_layerlet | 159.016 | 1.890 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 70 | fused_prologue_middle_layerlet | 159.900 | 1.881 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 75 | full_layerlet | 164.017 | 1.832 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 162.457 | 1.950 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 161.989 | 1.904 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 90 | full_layerlet | 164.892 | 1.880 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 167.024 | 1.887 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 161.113 | 1.909 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 105 | full_layerlet | 165.689 | 1.918 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 110 | full_layerlet | 163.627 | 1.922 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 162.344 | 1.883 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
