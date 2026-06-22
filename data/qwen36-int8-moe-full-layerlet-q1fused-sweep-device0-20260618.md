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

- Mean `xpu_fused_moe`: `317.881 us`.
- Mean scratch `xpu_fused_moe`: `262.305 us`.
- Mean preallocated staged: `203.725 us`.
- Mean fused-prologue staged: `276.484 us`.
- Mean fused-prologue offset-GEMM staged: `203.274 us`.
- Mean fused-prologue active-offset-GEMM staged: `204.481 us`.
- Mean fused-prologue middle-layerlet staged: `174.272 us`.
- Mean full C++ layerlet: `167.807 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 330.505 | 269.688 | 211.004 | 286.473 | 208.653 | 209.283 | 182.660 | 173.911 | 99.162 | 101.017 | 176.786 |
| 1 | 4 | 8 | 339.635 | 284.951 | 224.638 | 306.233 | 224.486 | 223.513 | 195.272 | 182.766 | 103.523 | 104.201 | 179.911 |
| 1 | 8 | 8 | 338.246 | 276.503 | 216.143 | 296.133 | 212.817 | 215.625 | 184.016 | 179.896 | 102.757 | 101.558 | 179.870 |
| 1 | 12 | 8 | 333.493 | 270.767 | 210.196 | 285.359 | 209.725 | 210.252 | 179.475 | 174.368 | 100.523 | 103.672 | 173.824 |
| 1 | 16 | 8 | 314.649 | 258.310 | 201.597 | 274.302 | 201.737 | 200.964 | 169.978 | 166.731 | 96.202 | 96.899 | 168.409 |
| 1 | 20 | 8 | 306.767 | 257.010 | 197.515 | 267.472 | 196.706 | 197.898 | 169.224 | 161.697 | 94.170 | 93.753 | 166.778 |
| 1 | 24 | 8 | 307.521 | 252.550 | 196.605 | 266.562 | 197.063 | 199.831 | 167.584 | 161.519 | 93.785 | 93.779 | 168.648 |
| 1 | 28 | 8 | 316.323 | 259.756 | 201.838 | 272.471 | 201.464 | 203.216 | 172.422 | 164.346 | 96.077 | 96.694 | 171.012 |
| 1 | 32 | 8 | 291.515 | 244.059 | 193.353 | 263.214 | 187.578 | 189.346 | 161.807 | 158.761 | 89.617 | 90.021 | 163.984 |
| 1 | 36 | 8 | 309.823 | 255.313 | 197.354 | 265.847 | 195.265 | 198.113 | 168.444 | 162.155 | 95.463 | 95.501 | 166.816 |
| 1 | 40 | 8 | 307.020 | 252.694 | 196.849 | 265.288 | 196.314 | 199.557 | 167.431 | 160.663 | 94.515 | 93.711 | 167.230 |
| 1 | 44 | 8 | 307.665 | 253.273 | 197.576 | 266.549 | 196.992 | 197.792 | 166.752 | 161.947 | 94.319 | 94.401 | 165.379 |
| 1 | 48 | 8 | 308.034 | 253.887 | 197.236 | 265.886 | 197.260 | 198.219 | 168.449 | 160.937 | 94.536 | 93.990 | 167.806 |
| 1 | 52 | 8 | 307.895 | 255.407 | 197.018 | 267.710 | 203.405 | 199.212 | 168.405 | 162.152 | 94.210 | 96.443 | 165.655 |
| 1 | 56 | 8 | 337.029 | 278.491 | 211.812 | 291.229 | 215.576 | 216.460 | 184.279 | 178.506 | 104.844 | 102.757 | 181.425 |
| 1 | 60 | 8 | 329.968 | 274.219 | 208.872 | 283.008 | 207.350 | 212.420 | 182.149 | 174.552 | 100.880 | 98.881 | 175.186 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `1` / `16`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `158.761 us` (`1.836x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 173.911 | 1.900 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | full_layerlet | 182.766 | 1.858 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | full_layerlet | 179.896 | 1.880 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | full_layerlet | 174.368 | 1.913 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | full_layerlet | 166.731 | 1.887 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | full_layerlet | 161.697 | 1.897 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | full_layerlet | 161.519 | 1.904 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | full_layerlet | 164.346 | 1.925 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | full_layerlet | 158.761 | 1.836 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 36 | full_layerlet | 162.155 | 1.911 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 160.663 | 1.911 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | full_layerlet | 161.947 | 1.900 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | full_layerlet | 160.937 | 1.914 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 52 | full_layerlet | 162.152 | 1.899 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | full_layerlet | 178.506 | 1.888 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 174.552 | 1.890 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
