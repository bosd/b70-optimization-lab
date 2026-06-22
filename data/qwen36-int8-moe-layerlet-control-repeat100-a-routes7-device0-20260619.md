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

- Mean `xpu_fused_moe`: `315.270 us`.
- Mean scratch `xpu_fused_moe`: `262.053 us`.
- Mean preallocated staged: `205.817 us`.
- Mean fused-prologue staged: `277.349 us`.
- Mean full C++ layerlet: `169.427 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 307.528 | 256.002 | 205.311 | 272.969 | n/a | n/a | n/a | 167.591 | 93.919 | 94.686 | 166.522 |
| 1 | 40 | 8 | 321.316 | 265.069 | 208.495 | 281.464 | n/a | n/a | n/a | 170.620 | 97.090 | 96.873 | 170.292 |
| 1 | 80 | 8 | 311.491 | 257.255 | 203.071 | 272.504 | n/a | n/a | n/a | 167.507 | 95.030 | 96.002 | 167.094 |
| 1 | 85 | 8 | 299.789 | 251.501 | 195.867 | 264.526 | n/a | n/a | n/a | 162.568 | 93.529 | 96.374 | 163.515 |
| 1 | 95 | 8 | 314.055 | 259.802 | 205.071 | 275.505 | n/a | n/a | n/a | 167.158 | 95.975 | 96.650 | 168.473 |
| 1 | 100 | 8 | 329.090 | 275.016 | 213.678 | 290.064 | n/a | n/a | n/a | 177.143 | 101.600 | 101.368 | 177.360 |
| 1 | 115 | 8 | 323.620 | 269.726 | 209.223 | 284.410 | n/a | n/a | n/a | 173.402 | 98.614 | 98.611 | 172.862 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `162.568 us` (`1.844x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 167.591 | 1.835 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 170.620 | 1.883 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 167.507 | 1.860 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 162.568 | 1.844 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 167.158 | 1.879 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 177.143 | 1.858 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 173.402 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
