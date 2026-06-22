# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `7`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `0,40,80,85,95,100,115`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `333.910 us`.
- Mean scratch `xpu_fused_moe`: `275.413 us`.
- Mean preallocated staged: `216.102 us`.
- Mean fused-prologue staged: `293.459 us`.
- Mean full C++ layerlet: `182.092 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 324.227 | 269.433 | 212.840 | 285.540 | n/a | n/a | n/a | 177.089 | 98.762 | 98.322 | 173.085 |
| 1 | 40 | 8 | 307.148 | 255.911 | 201.372 | 271.002 | n/a | n/a | n/a | 166.126 | 93.790 | 94.553 | 165.033 |
| 1 | 80 | 8 | 299.470 | 251.465 | 196.320 | 265.094 | n/a | n/a | n/a | 164.743 | 92.764 | 92.888 | 164.379 |
| 1 | 85 | 8 | 323.131 | 266.761 | 211.130 | 285.101 | n/a | n/a | n/a | 177.334 | 99.284 | 101.020 | 172.596 |
| 1 | 95 | 8 | 355.119 | 297.404 | 230.521 | 316.029 | n/a | n/a | n/a | 195.060 | 109.770 | 108.413 | 186.788 |
| 1 | 100 | 8 | 392.493 | 313.579 | 246.049 | 339.777 | n/a | n/a | n/a | 211.275 | 116.738 | 116.696 | 202.435 |
| 1 | 115 | 8 | 335.784 | 273.337 | 214.480 | 291.669 | n/a | n/a | n/a | 183.014 | 102.163 | 102.123 | 177.437 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `164.743 us` (`1.818x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 177.089 | 1.831 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 166.126 | 1.849 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 164.743 | 1.818 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 177.334 | 1.822 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 195.060 | 1.821 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 211.275 | 1.858 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 183.014 | 1.835 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
