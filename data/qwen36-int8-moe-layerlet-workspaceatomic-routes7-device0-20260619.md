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

- Mean `xpu_fused_moe`: `344.342 us`.
- Mean scratch `xpu_fused_moe`: `275.195 us`.
- Mean preallocated staged: `217.954 us`.
- Mean fused-prologue staged: `300.866 us`.
- Mean full C++ layerlet: `174.518 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 337.086 | 277.869 | 217.637 | 296.485 | n/a | n/a | n/a | 172.001 | 101.570 | 100.417 | 177.480 |
| 1 | 40 | 8 | 359.764 | 285.058 | 227.250 | 316.109 | n/a | n/a | n/a | 182.163 | 106.196 | 105.659 | 188.616 |
| 1 | 80 | 8 | 352.466 | 276.981 | 222.149 | 304.462 | n/a | n/a | n/a | 177.958 | 103.222 | 104.061 | 183.080 |
| 1 | 85 | 8 | 330.819 | 261.165 | 209.708 | 290.639 | n/a | n/a | n/a | 168.110 | 99.591 | 99.129 | 176.242 |
| 1 | 95 | 8 | 340.828 | 271.403 | 215.411 | 298.717 | n/a | n/a | n/a | 175.792 | 101.081 | 102.574 | 178.344 |
| 1 | 100 | 8 | 345.392 | 278.940 | 218.261 | 303.302 | n/a | n/a | n/a | 173.856 | 103.399 | 102.860 | 182.753 |
| 1 | 115 | 8 | 344.037 | 274.952 | 215.260 | 296.349 | n/a | n/a | n/a | 171.745 | 102.427 | 101.496 | 179.638 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `168.110 us` (`1.968x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 172.001 | 1.960 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 182.163 | 1.975 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 177.958 | 1.981 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 168.110 | 1.968 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 175.792 | 1.939 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 173.856 | 1.987 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 171.745 | 2.003 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
