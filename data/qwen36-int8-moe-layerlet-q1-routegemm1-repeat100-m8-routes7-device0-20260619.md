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

- Mean `xpu_fused_moe`: `329.600 us`.
- Mean scratch `xpu_fused_moe`: `272.952 us`.
- Mean preallocated staged: `213.229 us`.
- Mean fused-prologue staged: `288.544 us`.
- Mean full C++ layerlet: `177.547 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 303.762 | 251.688 | 199.155 | 266.878 | n/a | n/a | n/a | 167.137 | 95.032 | 96.153 | 163.271 |
| 1 | 40 | 8 | 314.487 | 261.006 | 205.534 | 277.757 | n/a | n/a | n/a | 169.889 | 97.669 | 97.595 | 169.220 |
| 1 | 80 | 8 | 315.131 | 263.208 | 203.455 | 276.261 | n/a | n/a | n/a | 168.974 | 97.925 | 98.002 | 172.960 |
| 1 | 85 | 8 | 366.260 | 296.810 | 232.020 | 315.745 | n/a | n/a | n/a | 196.220 | 112.575 | 110.826 | 194.367 |
| 1 | 95 | 8 | 317.847 | 263.951 | 205.625 | 278.974 | n/a | n/a | n/a | 169.780 | 98.588 | 100.895 | 170.148 |
| 1 | 100 | 8 | 299.674 | 251.411 | 196.864 | 265.023 | n/a | n/a | n/a | 165.230 | 94.258 | 94.203 | 168.112 |
| 1 | 115 | 8 | 390.037 | 322.592 | 249.952 | 339.168 | n/a | n/a | n/a | 205.600 | 119.041 | 118.163 | 203.156 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `165.230 us` (`1.814x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 167.137 | 1.817 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 169.889 | 1.851 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 168.974 | 1.865 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 196.220 | 1.867 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 169.780 | 1.872 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 165.230 | 1.814 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 205.600 | 1.897 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
