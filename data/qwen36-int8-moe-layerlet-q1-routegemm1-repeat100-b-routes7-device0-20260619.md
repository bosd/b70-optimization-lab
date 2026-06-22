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

- Mean `xpu_fused_moe`: `318.323 us`.
- Mean scratch `xpu_fused_moe`: `265.286 us`.
- Mean preallocated staged: `207.016 us`.
- Mean fused-prologue staged: `279.674 us`.
- Mean full C++ layerlet: `170.901 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 321.848 | 269.316 | 212.187 | 287.066 | n/a | n/a | n/a | 174.776 | 98.639 | 98.359 | 170.709 |
| 1 | 40 | 8 | 311.531 | 257.467 | 200.014 | 271.356 | n/a | n/a | n/a | 167.396 | 94.520 | 94.904 | 164.658 |
| 1 | 80 | 8 | 292.313 | 245.464 | 190.888 | 257.109 | n/a | n/a | n/a | 158.862 | 90.461 | 91.543 | 157.883 |
| 1 | 85 | 8 | 352.526 | 291.446 | 227.149 | 304.656 | n/a | n/a | n/a | 186.982 | 105.489 | 104.438 | 183.480 |
| 1 | 95 | 8 | 326.963 | 271.639 | 211.163 | 287.542 | n/a | n/a | n/a | 174.453 | 98.766 | 98.186 | 171.995 |
| 1 | 100 | 8 | 311.085 | 261.639 | 203.888 | 276.131 | n/a | n/a | n/a | 167.939 | 93.712 | 94.503 | 165.435 |
| 1 | 115 | 8 | 311.995 | 260.033 | 203.821 | 273.857 | n/a | n/a | n/a | 165.902 | 94.604 | 93.792 | 165.915 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `1` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `158.862 us` (`1.840x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 174.776 | 1.841 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 167.396 | 1.861 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 158.862 | 1.840 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 85 | full_layerlet | 186.982 | 1.885 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 174.453 | 1.874 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 167.939 | 1.852 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 165.902 | 1.881 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
