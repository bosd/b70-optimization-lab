# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- Full layerlet unchecked-middle enabled: `True`.
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

- Mean `xpu_fused_moe`: `331.124 us`.
- Mean scratch `xpu_fused_moe`: `270.599 us`.
- Mean preallocated staged: `210.678 us`.
- Mean fused-prologue staged: `288.530 us`.
- Mean fused-prologue offset-GEMM staged: `211.218 us`.
- Mean fused-prologue active-offset-GEMM staged: `213.150 us`.
- Mean fused-prologue middle-layerlet staged: `180.598 us`.
- Mean full C++ layerlet: `177.125 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 386.020 | 313.683 | 243.861 | 334.457 | 241.337 | 249.371 | 212.146 | 210.363 | 113.365 | 114.435 | 198.637 |
| 1 | 4 | 8 | 322.894 | 259.685 | 208.021 | 276.659 | 200.075 | 203.821 | 177.147 | 170.782 | 96.536 | 96.654 | 169.404 |
| 1 | 8 | 8 | 363.236 | 298.660 | 232.906 | 328.621 | 237.357 | 240.450 | 200.918 | 198.357 | 139.634 | 110.965 | 195.685 |
| 1 | 12 | 8 | 343.476 | 278.027 | 217.067 | 294.887 | 216.649 | 223.317 | 187.540 | 182.029 | 103.943 | 102.728 | 182.189 |
| 1 | 16 | 8 | 308.410 | 253.545 | 196.371 | 269.010 | 198.326 | 200.344 | 168.444 | 164.398 | 94.042 | 94.721 | 167.915 |
| 1 | 20 | 8 | 307.239 | 253.476 | 197.408 | 267.738 | 197.184 | 198.716 | 168.367 | 163.949 | 94.588 | 94.734 | 166.031 |
| 1 | 24 | 8 | 324.069 | 270.384 | 205.216 | 284.977 | 204.681 | 207.828 | 179.830 | 174.925 | 98.635 | 99.001 | 173.153 |
| 1 | 28 | 8 | 304.937 | 242.089 | 190.772 | 268.112 | 196.135 | 197.895 | 167.577 | 163.327 | 93.649 | 93.779 | 165.050 |
| 1 | 32 | 8 | 322.809 | 262.253 | 204.207 | 278.311 | 203.778 | 206.449 | 173.522 | 173.056 | 98.089 | 97.592 | 171.479 |
| 1 | 36 | 8 | 336.865 | 277.843 | 214.774 | 294.391 | 220.236 | 216.941 | 183.912 | 183.394 | 101.934 | 102.268 | 180.090 |
| 1 | 40 | 8 | 321.601 | 265.985 | 206.560 | 280.793 | 203.767 | 208.024 | 175.611 | 169.700 | 99.169 | 100.487 | 175.673 |
| 1 | 44 | 8 | 306.675 | 253.720 | 197.817 | 270.107 | 197.515 | 199.846 | 166.878 | 164.389 | 94.227 | 94.848 | 166.598 |
| 1 | 48 | 8 | 322.960 | 260.054 | 201.753 | 275.931 | 202.074 | 206.040 | 172.047 | 168.142 | 97.079 | 96.737 | 170.210 |
| 1 | 52 | 8 | 323.118 | 263.385 | 206.875 | 281.502 | 206.794 | 208.444 | 177.332 | 173.205 | 98.571 | 98.961 | 172.853 |
| 1 | 56 | 8 | 361.298 | 302.011 | 232.950 | 319.847 | 239.777 | 230.844 | 195.740 | 194.724 | 110.091 | 114.008 | 196.073 |
| 1 | 60 | 8 | 342.384 | 274.777 | 214.285 | 291.136 | 213.805 | 212.068 | 182.560 | 179.253 | 102.906 | 103.140 | 184.609 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `16`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `163.327 us` (`1.867x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 210.363 | 1.835 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | full_layerlet | 170.782 | 1.891 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | full_layerlet | 198.357 | 1.831 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | full_layerlet | 182.029 | 1.887 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | full_layerlet | 164.398 | 1.876 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 163.949 | 1.874 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | full_layerlet | 174.925 | 1.853 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | full_layerlet | 163.327 | 1.867 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | full_layerlet | 173.056 | 1.865 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | full_layerlet | 183.394 | 1.837 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 169.700 | 1.895 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | full_layerlet | 164.389 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | full_layerlet | 168.142 | 1.921 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 52 | full_layerlet | 173.205 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | full_layerlet | 194.724 | 1.855 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 179.253 | 1.910 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
