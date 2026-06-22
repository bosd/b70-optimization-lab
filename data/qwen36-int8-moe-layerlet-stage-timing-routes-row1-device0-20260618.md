# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `7`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-firstdecode-route-fixture-routes-20260612ct.jsonl`.
- Route records matched: `120`; top-k rows loaded: `120`.
- Route start indices: `0,40,80,85,95,100,115`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Fused-prologue offset-GEMM max abs diff: `0.000`.
- Fused-prologue active-offset-GEMM max abs diff: `0.000`.
- Fused-prologue middle-layerlet max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `315.284 us`.
- Mean scratch `xpu_fused_moe`: `256.246 us`.
- Mean preallocated staged: `199.890 us`.
- Mean fused-prologue staged: `272.911 us`.
- Mean fused-prologue offset-GEMM staged: `198.816 us`.
- Mean fused-prologue active-offset-GEMM staged: `200.850 us`.
- Mean fused-prologue middle-layerlet staged: `169.940 us`.
- Mean full C++ layerlet: `166.003 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 303.953 | 251.259 | 193.503 | 263.899 | 198.245 | 193.332 | 164.361 | 160.087 | 92.342 | 92.981 | 167.885 |
| 1 | 40 | 8 | 306.356 | 252.554 | 195.028 | 265.778 | 192.943 | 197.368 | 165.540 | 158.852 | 100.474 | 92.507 | 164.965 |
| 1 | 80 | 8 | 294.075 | 243.075 | 189.884 | 258.991 | 186.573 | 189.505 | 159.823 | 157.465 | 91.945 | 90.877 | 158.536 |
| 1 | 85 | 8 | 297.436 | 245.806 | 187.825 | 256.538 | 187.538 | 189.109 | 162.321 | 155.219 | 91.463 | 91.132 | 158.639 |
| 1 | 95 | 8 | 318.257 | 259.557 | 203.865 | 273.078 | 197.177 | 204.925 | 171.677 | 169.892 | 96.037 | 96.821 | 169.830 |
| 1 | 100 | 8 | 342.872 | 271.882 | 214.175 | 297.017 | 214.082 | 217.510 | 184.064 | 178.837 | 102.274 | 102.809 | 179.573 |
| 1 | 115 | 8 | 344.042 | 269.590 | 214.948 | 295.071 | 215.154 | 214.201 | 181.797 | 181.672 | 102.654 | 102.469 | 178.101 |

## Prologue Offset Stage Timing

These stage timings are for the exact fused-prologue offset-GEMM candidate and are used to decide the next native layerlet boundary. They are single-device replay diagnostics.

| rows | route start | total us | prologue | quant1 | gemm1 | activation | quant2 | gemm2 | gather | component sum |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 198.245 | 103.195 | 80.307 | 95.271 | 76.224 | 79.602 | 94.703 | 79.180 | 608.482 |
| 1 | 40 | 192.943 | 103.810 | 79.690 | 94.648 | 77.450 | 79.588 | 94.755 | 79.401 | 609.344 |
| 1 | 80 | 186.573 | 99.023 | 76.284 | 90.068 | 73.206 | 75.555 | 89.753 | 75.787 | 579.675 |
| 1 | 85 | 187.538 | 98.591 | 76.435 | 90.224 | 72.432 | 76.357 | 90.846 | 74.138 | 579.023 |
| 1 | 95 | 197.177 | 105.620 | 82.380 | 99.260 | 78.953 | 81.159 | 96.786 | 79.185 | 623.343 |
| 1 | 100 | 214.082 | 100.112 | 78.346 | 92.401 | 73.120 | 76.430 | 90.323 | 75.638 | 586.370 |
| 1 | 115 | 215.154 | 127.526 | 96.456 | 118.388 | 93.307 | 97.250 | 118.615 | 94.880 | 746.422 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `3` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `155.219 us` (`1.916x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 160.087 | 1.899 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 158.852 | 1.929 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 80 | full_layerlet | 157.465 | 1.868 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 85 | full_layerlet | 155.219 | 1.916 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 95 | full_layerlet | 169.892 | 1.873 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 178.837 | 1.917 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 181.672 | 1.894 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
