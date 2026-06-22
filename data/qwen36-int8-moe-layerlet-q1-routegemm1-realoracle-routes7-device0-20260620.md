# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `7`.
- Route mode/source: `route_jsonl`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `0,40,80,85,95,100,115`.
- Prologue-inclusive target: `160.000 us/layerlet`.
- Exactness threshold: `0.000000`.

## Exactness

- Manual staged max abs diff versus `xpu_fused_moe`: `0.000`.
- Scratch `xpu_fused_moe` max abs diff: `0.000`.
- Prologue-scratch `xpu_fused_moe` max abs diff: `0.000`.
- Preallocated staged max abs diff: `0.000`.
- Fused-prologue staged max abs diff: `0.000`.
- Full C++ layerlet max abs diff: `0.000`.

### Rows-Oracle Checks

- Current `xpu_fused_moe` max abs diff versus forced rows-per-expert oracle: `0.000`.
- Forced offset-GEMM max abs diff versus rows-per-expert oracle: `0.000`.
- Full C++ layerlet max abs diff versus rows-per-expert oracle: `0.000`.

## Timing

- Mean `xpu_fused_moe`: `339.209 us`.
- Mean scratch `xpu_fused_moe`: `273.406 us`.
- Mean prologue-scratch `xpu_fused_moe`: `276.932 us`.
- Mean preallocated staged: `219.245 us`.
- Mean fused-prologue staged: `296.684 us`.
- Mean full C++ layerlet: `180.195 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | xpu prologue scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | oneDNN sidecar us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 330.166 | 259.807 | 267.051 | 216.447 | 288.974 | n/a | n/a | n/a | 174.831 | n/a | 98.784 | 98.531 | 172.472 |
| 1 | 40 | 8 | 337.293 | 265.949 | 272.286 | 218.638 | 294.157 | n/a | n/a | n/a | 177.419 | n/a | 101.104 | 100.448 | 175.805 |
| 1 | 80 | 8 | 366.165 | 293.275 | 298.719 | 237.079 | 317.677 | n/a | n/a | n/a | 192.927 | n/a | 108.559 | 109.021 | 190.353 |
| 1 | 85 | 8 | 324.549 | 267.864 | 266.419 | 206.872 | 281.666 | n/a | n/a | n/a | 175.451 | n/a | 98.421 | 98.806 | 171.958 |
| 1 | 95 | 8 | 332.264 | 268.966 | 273.289 | 215.658 | 293.444 | n/a | n/a | n/a | 176.264 | n/a | 99.442 | 100.429 | 174.201 |
| 1 | 100 | 8 | 349.122 | 287.747 | 288.286 | 224.867 | 308.762 | n/a | n/a | n/a | 187.057 | n/a | 104.620 | 105.019 | 183.235 |
| 1 | 115 | 8 | 334.906 | 270.234 | 272.477 | 215.156 | 292.104 | n/a | n/a | n/a | 177.413 | n/a | 101.236 | 100.481 | 175.581 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `7`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `174.831 us` (`1.888x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | full_layerlet | 174.831 | 1.888 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | full_layerlet | 177.419 | 1.901 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 80 | full_layerlet | 192.927 | 1.898 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 85 | full_layerlet | 175.451 | 1.850 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 95 | full_layerlet | 176.264 | 1.885 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 100 | full_layerlet | 187.057 | 1.866 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 115 | full_layerlet | 177.413 | 1.888 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
