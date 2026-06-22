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

- Mean `xpu_fused_moe`: `326.934 us`.
- Mean scratch `xpu_fused_moe`: `265.470 us`.
- Mean preallocated staged: `209.992 us`.
- Mean fused-prologue staged: `285.788 us`.
- Mean full C++ layerlet: `174.773 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 337.771 | 278.120 | 220.105 | 296.897 | n/a | n/a | n/a | 181.707 | 100.593 | 100.925 | 176.209 |
| 1 | 40 | 8 | 330.307 | 274.773 | 213.937 | 290.818 | n/a | n/a | n/a | 177.906 | 99.926 | 100.165 | 174.400 |
| 1 | 80 | 8 | 331.607 | 275.443 | 214.272 | 291.229 | n/a | n/a | n/a | 179.215 | 101.380 | 101.341 | 174.776 |
| 1 | 85 | 8 | 351.780 | 286.941 | 225.444 | 304.843 | n/a | n/a | n/a | 185.706 | 107.991 | 106.062 | 187.383 |
| 1 | 95 | 8 | 309.334 | 247.415 | 196.801 | 269.917 | n/a | n/a | n/a | 166.685 | 95.235 | 96.469 | 167.991 |
| 1 | 100 | 8 | 315.051 | 246.633 | 200.238 | 274.942 | n/a | n/a | n/a | 166.607 | 94.992 | 95.685 | 167.445 |
| 1 | 115 | 8 | 312.689 | 248.967 | 199.146 | 271.871 | n/a | n/a | n/a | 165.580 | 94.311 | 94.303 | 168.317 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `165.580 us` (`1.888x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 181.707 | 1.859 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 177.906 | 1.857 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 179.215 | 1.850 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 185.706 | 1.894 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 166.685 | 1.856 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 166.607 | 1.891 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 165.580 | 1.888 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
