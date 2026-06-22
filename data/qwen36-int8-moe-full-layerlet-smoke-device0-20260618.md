# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `3`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `52,56,60`.
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

## Timing

- Mean `xpu_fused_moe`: `334.743 us`.
- Mean scratch `xpu_fused_moe`: `271.565 us`.
- Mean preallocated staged: `212.294 us`.
- Mean fused-prologue staged: `290.963 us`.
- Mean fused-prologue offset-GEMM staged: `213.115 us`.
- Mean fused-prologue active-offset-GEMM staged: `214.511 us`.
- Mean fused-prologue middle-layerlet staged: `182.790 us`.
- Mean full C++ layerlet: `175.769 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | full layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 52 | 8 | 326.709 | 271.447 | 211.998 | 288.703 | 211.044 | 211.154 | 176.200 | 170.938 | 98.961 | 98.489 | 173.634 |
| 1 | 56 | 8 | 323.823 | 264.380 | 206.761 | 281.076 | 206.940 | 209.610 | 182.630 | 171.740 | 97.024 | 101.269 | 170.047 |
| 1 | 60 | 8 | 353.699 | 278.868 | 218.123 | 303.110 | 221.362 | 222.769 | 189.540 | 184.628 | 104.472 | 104.219 | 180.114 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `3`.
- Best exact non-reference full-layerlet candidate: `full_layerlet` at `170.938 us` (`1.911x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 52 | full_layerlet | 170.938 | 1.911 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | full_layerlet | 171.740 | 1.886 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | full_layerlet | 184.628 | 1.916 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
