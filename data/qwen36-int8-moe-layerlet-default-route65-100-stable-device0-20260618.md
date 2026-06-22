# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `2`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-firstdecode-route-fixture-routes-20260612ct.jsonl`.
- Route records matched: `120`; top-k rows loaded: `120`.
- Route start indices: `65,100`.
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

- Mean `xpu_fused_moe`: `303.626 us`.
- Mean scratch `xpu_fused_moe`: `251.515 us`.
- Mean preallocated staged: `198.695 us`.
- Mean fused-prologue staged: `267.072 us`.
- Mean fused-prologue offset-GEMM staged: `196.664 us`.
- Mean fused-prologue active-offset-GEMM staged: `196.702 us`.
- Mean fused-prologue middle-layerlet staged: `167.390 us`.
- Mean full C++ layerlet: `164.051 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 65 | 8 | 313.952 | 260.589 | 206.281 | 275.777 | 204.303 | 203.441 | 172.207 | 169.738 | 96.509 | 96.292 | 171.168 |
| 1 | 100 | 8 | 293.301 | 242.441 | 191.110 | 258.367 | 189.025 | 189.963 | 162.573 | 158.364 | 91.541 | 91.499 | 161.743 |

## Prologue Offset Stage Timing

These stage timings are for the exact fused-prologue offset-GEMM candidate and are used to decide the next native layerlet boundary. They are single-device replay diagnostics.

| rows | route start | total us | prologue | quant1 | gemm1 | activation | quant2 | gemm2 | gather | component sum |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 65 | 204.303 | 100.329 | 76.570 | 91.447 | 74.568 | 76.133 | 90.724 | 75.811 | 585.582 |
| 1 | 100 | 189.025 | 101.811 | 77.116 | 90.974 | 73.908 | 75.520 | 88.639 | 75.358 | 583.326 |

## Prologue-Inclusive Gate

- Gate status: `some_rows_have_exact_nonreference_layerlet_candidate`.
- Rows ready for endpoint gate: `1` / `2`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `158.364 us` (`1.852x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 65 | full_layerlet | 169.738 | 1.850 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 158.364 | 1.852 | True | candidate_layerlet_meets_speed_and_exactness_gate |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
