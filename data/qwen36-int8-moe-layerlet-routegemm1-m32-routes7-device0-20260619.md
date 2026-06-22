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

- Mean `xpu_fused_moe`: `324.565 us`.
- Mean scratch `xpu_fused_moe`: `267.773 us`.
- Mean preallocated staged: `209.055 us`.
- Mean fused-prologue staged: `285.571 us`.
- Mean full C++ layerlet: `175.938 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 354.287 | 291.366 | 227.536 | 307.484 | n/a | n/a | n/a | 190.081 | 108.229 | 108.328 | 189.010 |
| 1 | 40 | 8 | 314.733 | 258.724 | 201.782 | 275.230 | n/a | n/a | n/a | 171.121 | 96.909 | 96.991 | 171.102 |
| 1 | 80 | 8 | 299.841 | 250.481 | 195.009 | 265.152 | n/a | n/a | n/a | 164.655 | 94.989 | 95.308 | 167.009 |
| 1 | 85 | 8 | 367.957 | 302.987 | 236.283 | 321.928 | n/a | n/a | n/a | 198.761 | 113.457 | 113.001 | 197.284 |
| 1 | 95 | 8 | 305.304 | 253.616 | 198.109 | 274.761 | n/a | n/a | n/a | 164.451 | 93.564 | 93.980 | 166.147 |
| 1 | 100 | 8 | 297.645 | 248.763 | 194.564 | 263.241 | n/a | n/a | n/a | 162.336 | 93.227 | 93.254 | 162.425 |
| 1 | 115 | 8 | 332.191 | 268.470 | 210.102 | 291.204 | n/a | n/a | n/a | 180.162 | 100.540 | 101.236 | 175.333 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `162.336 us` (`1.834x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 190.081 | 1.864 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 171.121 | 1.839 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 164.655 | 1.821 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 198.761 | 1.851 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 164.451 | 1.857 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 162.336 | 1.834 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 180.162 | 1.844 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
