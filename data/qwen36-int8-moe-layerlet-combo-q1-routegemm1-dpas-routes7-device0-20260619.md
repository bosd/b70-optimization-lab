# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `7`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
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

- Mean `xpu_fused_moe`: `314.271 us`.
- Mean scratch `xpu_fused_moe`: `261.455 us`.
- Mean preallocated staged: `203.161 us`.
- Mean fused-prologue staged: `274.898 us`.
- Mean full C++ layerlet: `167.490 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 325.624 | 271.956 | 214.075 | 288.064 | n/a | n/a | n/a | 173.997 | 100.217 | 99.865 | 171.454 |
| 1 | 40 | 8 | 381.014 | 305.943 | 239.181 | 331.909 | n/a | n/a | n/a | 196.863 | 111.161 | 113.523 | 198.257 |
| 1 | 80 | 8 | 297.702 | 246.997 | 192.273 | 258.365 | n/a | n/a | n/a | 159.464 | 89.516 | 90.141 | 159.040 |
| 1 | 85 | 8 | 294.518 | 254.085 | 192.247 | 258.385 | n/a | n/a | n/a | 158.374 | 89.512 | 91.791 | 156.624 |
| 1 | 95 | 8 | 294.516 | 246.374 | 192.433 | 259.050 | n/a | n/a | n/a | 159.085 | 89.918 | 90.396 | 158.700 |
| 1 | 100 | 8 | 310.971 | 258.212 | 199.845 | 270.106 | n/a | n/a | n/a | 165.793 | 93.653 | 93.629 | 163.521 |
| 1 | 115 | 8 | 295.548 | 246.619 | 192.072 | 258.407 | n/a | n/a | n/a | 158.852 | 89.705 | 89.922 | 159.089 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `4` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `158.374 us` (`1.860x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 173.997 | 1.871 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 196.863 | 1.935 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 159.464 | 1.867 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 85 | full_layerlet | 158.374 | 1.860 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 95 | full_layerlet | 159.085 | 1.851 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 100 | full_layerlet | 165.793 | 1.876 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 158.852 | 1.861 | True | candidate_layerlet_meets_speed_and_exactness_gate |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
