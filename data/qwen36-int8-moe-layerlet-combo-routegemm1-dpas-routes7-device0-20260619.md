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

- Mean `xpu_fused_moe`: `317.508 us`.
- Mean scratch `xpu_fused_moe`: `263.847 us`.
- Mean preallocated staged: `207.373 us`.
- Mean fused-prologue staged: `280.740 us`.
- Mean full C++ layerlet: `172.354 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 290.787 | 244.003 | 193.954 | 259.700 | n/a | n/a | n/a | 159.388 | 89.827 | 89.781 | 160.607 |
| 1 | 40 | 8 | 337.029 | 284.755 | 221.707 | 307.252 | n/a | n/a | n/a | 183.670 | 102.537 | 102.783 | 180.905 |
| 1 | 80 | 8 | 329.911 | 273.029 | 213.557 | 287.688 | n/a | n/a | n/a | 178.567 | 98.670 | 99.171 | 177.275 |
| 1 | 85 | 8 | 316.917 | 260.770 | 206.523 | 277.740 | n/a | n/a | n/a | 171.568 | 95.560 | 95.794 | 170.852 |
| 1 | 95 | 8 | 316.708 | 260.822 | 205.520 | 278.043 | n/a | n/a | n/a | 170.725 | 95.928 | 95.854 | 169.236 |
| 1 | 100 | 8 | 305.896 | 253.244 | 198.186 | 269.587 | n/a | n/a | n/a | 166.361 | 93.187 | 96.619 | 166.931 |
| 1 | 115 | 8 | 325.306 | 270.304 | 212.164 | 285.167 | n/a | n/a | n/a | 176.199 | 98.231 | 98.930 | 175.590 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `1` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `159.388 us` (`1.824x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 159.388 | 1.824 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 40 | full_layerlet | 183.670 | 1.835 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 178.567 | 1.848 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 171.568 | 1.847 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 170.725 | 1.855 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 166.361 | 1.839 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 176.199 | 1.846 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
