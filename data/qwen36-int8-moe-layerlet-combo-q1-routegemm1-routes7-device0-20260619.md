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

- Mean `xpu_fused_moe`: `295.175 us`.
- Mean scratch `xpu_fused_moe`: `245.363 us`.
- Mean preallocated staged: `192.940 us`.
- Mean fused-prologue staged: `260.663 us`.
- Mean full C++ layerlet: `159.864 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 291.420 | 243.478 | 193.978 | 260.086 | n/a | n/a | n/a | 158.337 | 90.145 | 91.343 | 158.549 |
| 1 | 40 | 8 | 292.380 | 242.189 | 190.531 | 257.645 | n/a | n/a | n/a | 158.479 | 90.125 | 90.047 | 157.792 |
| 1 | 80 | 8 | 320.583 | 262.723 | 205.557 | 277.930 | n/a | n/a | n/a | 171.398 | 97.068 | 95.971 | 171.213 |
| 1 | 85 | 8 | 291.421 | 243.367 | 190.681 | 257.520 | n/a | n/a | n/a | 157.696 | 89.534 | 89.722 | 158.808 |
| 1 | 95 | 8 | 289.828 | 241.991 | 189.465 | 257.000 | n/a | n/a | n/a | 157.323 | 89.508 | 90.036 | 156.895 |
| 1 | 100 | 8 | 290.514 | 242.047 | 190.349 | 257.091 | n/a | n/a | n/a | 157.864 | 89.296 | 89.197 | 156.972 |
| 1 | 115 | 8 | 290.075 | 241.750 | 190.024 | 257.371 | n/a | n/a | n/a | 157.953 | 89.493 | 90.680 | 157.242 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `6` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `157.323 us` (`1.842x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 158.337 | 1.841 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 40 | full_layerlet | 158.479 | 1.845 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 80 | full_layerlet | 171.398 | 1.870 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 157.696 | 1.848 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 95 | full_layerlet | 157.323 | 1.842 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 100 | full_layerlet | 157.864 | 1.840 | True | candidate_layerlet_meets_speed_and_exactness_gate |
| 1 | 115 | full_layerlet | 157.953 | 1.836 | True | candidate_layerlet_meets_speed_and_exactness_gate |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
