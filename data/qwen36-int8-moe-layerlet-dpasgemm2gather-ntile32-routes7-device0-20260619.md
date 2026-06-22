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

- Mean `xpu_fused_moe`: `324.559 us`.
- Mean scratch `xpu_fused_moe`: `268.879 us`.
- Mean preallocated staged: `210.998 us`.
- Mean fused-prologue staged: `286.559 us`.
- Mean full C++ layerlet: `176.388 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 349.052 | 287.646 | 227.133 | 309.675 | n/a | n/a | n/a | 189.810 | 106.853 | 105.605 | 188.803 |
| 1 | 40 | 8 | 312.865 | 261.754 | 203.224 | 276.679 | n/a | n/a | n/a | 170.550 | 96.336 | 96.392 | 168.728 |
| 1 | 80 | 8 | 315.816 | 263.008 | 206.278 | 280.422 | n/a | n/a | n/a | 172.427 | 98.110 | 97.549 | 171.936 |
| 1 | 85 | 8 | 321.651 | 267.184 | 208.705 | 282.709 | n/a | n/a | n/a | 173.695 | 98.573 | 98.417 | 173.205 |
| 1 | 95 | 8 | 334.873 | 274.636 | 216.254 | 295.315 | n/a | n/a | n/a | 181.888 | 102.283 | 102.554 | 182.651 |
| 1 | 100 | 8 | 321.295 | 265.267 | 209.636 | 282.140 | n/a | n/a | n/a | 174.023 | 99.524 | 98.097 | 172.358 |
| 1 | 115 | 8 | 316.360 | 262.655 | 205.758 | 278.975 | n/a | n/a | n/a | 172.322 | 97.539 | 97.261 | 170.918 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `170.550 us` (`1.834x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 189.810 | 1.839 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 170.550 | 1.834 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 172.427 | 1.832 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 173.695 | 1.852 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 181.888 | 1.841 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 174.023 | 1.846 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 172.322 | 1.836 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
