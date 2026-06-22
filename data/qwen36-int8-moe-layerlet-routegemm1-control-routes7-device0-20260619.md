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

- Mean `xpu_fused_moe`: `307.738 us`.
- Mean scratch `xpu_fused_moe`: `252.677 us`.
- Mean preallocated staged: `199.577 us`.
- Mean fused-prologue staged: `270.404 us`.
- Mean full C++ layerlet: `165.677 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 300.335 | 250.323 | 198.139 | 264.753 | n/a | n/a | n/a | 162.311 | 91.944 | 93.034 | 164.042 |
| 1 | 40 | 8 | 308.674 | 255.901 | 200.873 | 272.018 | n/a | n/a | n/a | 166.755 | 95.099 | 95.279 | 163.881 |
| 1 | 80 | 8 | 317.941 | 259.901 | 204.892 | 278.410 | n/a | n/a | n/a | 170.076 | 95.592 | 95.835 | 167.496 |
| 1 | 85 | 8 | 307.590 | 253.885 | 200.793 | 270.135 | n/a | n/a | n/a | 166.611 | 93.697 | 94.883 | 165.338 |
| 1 | 95 | 8 | 312.967 | 247.919 | 196.545 | 275.089 | n/a | n/a | n/a | 167.100 | 94.426 | 94.717 | 165.047 |
| 1 | 100 | 8 | 308.683 | 253.833 | 201.958 | 270.554 | n/a | n/a | n/a | 165.555 | 93.699 | 95.190 | 166.202 |
| 1 | 115 | 8 | 297.973 | 246.977 | 193.837 | 261.867 | n/a | n/a | n/a | 161.335 | 92.502 | 91.584 | 160.000 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `161.335 us` (`1.847x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 162.311 | 1.850 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 166.755 | 1.851 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 170.076 | 1.869 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 166.611 | 1.846 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 167.100 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 165.555 | 1.865 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 161.335 | 1.847 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
