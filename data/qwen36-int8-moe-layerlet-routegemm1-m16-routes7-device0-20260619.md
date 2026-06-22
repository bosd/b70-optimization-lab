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

- Mean `xpu_fused_moe`: `303.100 us`.
- Mean scratch `xpu_fused_moe`: `253.375 us`.
- Mean preallocated staged: `197.730 us`.
- Mean fused-prologue staged: `267.691 us`.
- Mean full C++ layerlet: `165.340 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 317.426 | 263.113 | 206.651 | 277.525 | n/a | n/a | n/a | 173.424 | 97.453 | 96.588 | 169.933 |
| 1 | 40 | 8 | 305.921 | 256.698 | 200.550 | 272.307 | n/a | n/a | n/a | 167.312 | 95.015 | 95.373 | 166.751 |
| 1 | 80 | 8 | 297.368 | 248.814 | 193.846 | 262.670 | n/a | n/a | n/a | 162.484 | 92.103 | 91.862 | 163.156 |
| 1 | 85 | 8 | 298.624 | 251.752 | 196.353 | 265.268 | n/a | n/a | n/a | 163.872 | 93.344 | 94.077 | 165.148 |
| 1 | 95 | 8 | 302.609 | 252.062 | 196.360 | 267.148 | n/a | n/a | n/a | 163.861 | 94.298 | 93.390 | 164.578 |
| 1 | 100 | 8 | 301.045 | 252.462 | 196.408 | 266.252 | n/a | n/a | n/a | 164.664 | 93.777 | 93.846 | 165.167 |
| 1 | 115 | 8 | 298.711 | 248.725 | 193.943 | 262.668 | n/a | n/a | n/a | 161.763 | 92.231 | 93.506 | 163.383 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `161.763 us` (`1.847x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 173.424 | 1.830 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 167.312 | 1.828 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 162.484 | 1.830 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 163.872 | 1.822 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 163.861 | 1.847 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 164.664 | 1.828 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 161.763 | 1.847 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
