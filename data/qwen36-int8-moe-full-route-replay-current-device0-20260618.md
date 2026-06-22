# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `16`.
- Quant out-variant available: `True`.
- Route source: `data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `308.363 us`.
- Mean scratch `xpu_fused_moe`: `256.104 us`.
- Mean preallocated staged: `200.261 us`.
- Mean fused-prologue staged: `270.232 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 312.016 | 264.436 | 201.817 | 272.679 | n/a | n/a | 94.432 | 97.046 | 172.316 |
| 1 | 4 | 8 | 304.216 | 250.617 | 195.983 | 264.793 | n/a | n/a | 93.356 | 93.092 | 165.017 |
| 1 | 8 | 8 | 308.261 | 255.651 | 201.360 | 269.811 | n/a | n/a | 94.560 | 94.969 | 166.637 |
| 1 | 12 | 8 | 299.536 | 247.679 | 197.685 | 264.243 | n/a | n/a | 92.669 | 93.985 | 169.598 |
| 1 | 16 | 8 | 306.954 | 251.935 | 199.616 | 283.901 | n/a | n/a | 94.810 | 94.806 | 166.885 |
| 1 | 20 | 8 | 300.465 | 254.646 | 197.099 | 263.687 | n/a | n/a | 92.761 | 93.503 | 164.382 |
| 1 | 24 | 8 | 309.131 | 253.904 | 200.860 | 267.784 | n/a | n/a | 93.896 | 94.080 | 165.842 |
| 1 | 28 | 8 | 310.050 | 255.674 | 199.382 | 268.285 | n/a | n/a | 94.848 | 94.299 | 167.638 |
| 1 | 32 | 8 | 305.750 | 253.949 | 199.399 | 267.412 | n/a | n/a | 94.351 | 94.846 | 164.989 |
| 1 | 36 | 8 | 327.832 | 274.638 | 212.002 | 286.749 | n/a | n/a | 99.512 | 99.518 | 177.105 |
| 1 | 40 | 8 | 307.698 | 255.941 | 199.550 | 268.008 | n/a | n/a | 94.380 | 94.396 | 167.502 |
| 1 | 44 | 8 | 291.952 | 243.502 | 191.159 | 255.622 | n/a | n/a | 90.643 | 90.116 | 159.486 |
| 1 | 48 | 8 | 308.415 | 256.603 | 199.813 | 269.920 | n/a | n/a | 94.687 | 94.995 | 167.989 |
| 1 | 52 | 8 | 304.398 | 252.951 | 198.420 | 266.235 | n/a | n/a | 93.993 | 93.865 | 165.648 |
| 1 | 56 | 8 | 309.705 | 255.800 | 199.997 | 270.007 | n/a | n/a | 94.368 | 95.319 | 166.830 |
| 1 | 60 | 8 | 327.434 | 269.733 | 210.037 | 284.575 | n/a | n/a | 99.703 | 101.298 | 176.616 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `16`.
- Best exact non-reference full-layerlet candidate: `preallocated_staged` at `191.159 us` (`1.527x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | preallocated_staged | 201.817 | 1.546 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | preallocated_staged | 195.983 | 1.552 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | preallocated_staged | 201.360 | 1.531 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | preallocated_staged | 197.685 | 1.515 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | preallocated_staged | 199.616 | 1.538 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | preallocated_staged | 197.099 | 1.524 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | preallocated_staged | 200.860 | 1.539 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | preallocated_staged | 199.382 | 1.555 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | preallocated_staged | 199.399 | 1.533 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | preallocated_staged | 212.002 | 1.546 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | preallocated_staged | 199.550 | 1.542 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | preallocated_staged | 191.159 | 1.527 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | preallocated_staged | 199.813 | 1.544 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 52 | preallocated_staged | 198.420 | 1.534 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | preallocated_staged | 199.997 | 1.549 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | preallocated_staged | 210.037 | 1.559 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
