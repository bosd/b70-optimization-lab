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

- Mean `xpu_fused_moe`: `327.825 us`.
- Mean scratch `xpu_fused_moe`: `270.173 us`.
- Mean preallocated staged: `211.666 us`.
- Mean fused-prologue staged: `288.066 us`.
- Mean full C++ layerlet: `176.882 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 347.451 | 287.255 | 224.104 | 307.327 | n/a | n/a | n/a | 188.642 | 104.842 | 105.570 | 184.652 |
| 1 | 40 | 8 | 337.798 | 277.624 | 216.421 | 296.299 | n/a | n/a | n/a | 181.233 | 103.700 | 102.527 | 179.197 |
| 1 | 80 | 8 | 334.434 | 273.822 | 216.269 | 292.504 | n/a | n/a | n/a | 179.209 | 100.723 | 100.435 | 174.835 |
| 1 | 85 | 8 | 310.472 | 256.344 | 200.504 | 271.953 | n/a | n/a | n/a | 167.183 | 94.060 | 94.632 | 165.222 |
| 1 | 95 | 8 | 326.216 | 271.499 | 212.635 | 288.673 | n/a | n/a | n/a | 177.742 | 98.416 | 98.249 | 171.696 |
| 1 | 100 | 8 | 322.988 | 266.095 | 209.229 | 283.926 | n/a | n/a | n/a | 175.294 | 97.997 | 98.007 | 173.323 |
| 1 | 115 | 8 | 315.417 | 258.568 | 202.504 | 275.780 | n/a | n/a | n/a | 168.871 | 95.322 | 94.917 | 166.733 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `167.183 us` (`1.857x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 188.642 | 1.842 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 181.233 | 1.864 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 179.209 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 167.183 | 1.857 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 177.742 | 1.835 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 175.294 | 1.843 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 168.871 | 1.868 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
