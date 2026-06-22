# Qwen3.6 INT8 MoE Route Replay

- Fused SiLU+quant enabled: `False`.
- TP size: `4`.
- Result rows: `16`.
- Quant out-variant available: `True`.
- Route source: `/home/steve/llm-optimizations/data/qwen36-quark-int8-tp4-routecapture6-routes-rank0-20260611.jsonl`.
- Route records matched: `95`; top-k rows loaded: `95`.
- Route start indices: `0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60`.
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

## Timing

- Mean `xpu_fused_moe`: `309.249 us`.
- Mean scratch `xpu_fused_moe`: `256.626 us`.
- Mean preallocated staged: `199.703 us`.
- Mean fused-prologue staged: `271.566 us`.
- Mean fused-prologue offset-GEMM staged: `198.030 us`.
- Mean fused-prologue active-offset-GEMM staged: `200.152 us`.
- Mean fused-prologue middle-layerlet staged: `169.232 us`.

| rows | route start | active experts | xpu fused us | xpu scratch us | prealloc staged us | fused prologue staged us | fused prologue offset us | active offset us | middle layerlet us | gemm1 us | gemm2 us | act+quant2 us |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 8 | 311.575 | 253.575 | 197.928 | 268.921 | 195.615 | 197.512 | 168.158 | 93.572 | 93.976 | 165.838 |
| 1 | 4 | 8 | 312.778 | 259.447 | 202.689 | 274.116 | 200.018 | 202.812 | 171.565 | 95.226 | 95.786 | 168.574 |
| 1 | 8 | 8 | 326.888 | 270.818 | 209.758 | 291.328 | 209.503 | 213.020 | 177.502 | 120.812 | 100.277 | 186.085 |
| 1 | 12 | 8 | 310.710 | 254.185 | 200.684 | 271.944 | 199.930 | 201.068 | 169.926 | 94.666 | 94.517 | 167.218 |
| 1 | 16 | 8 | 309.967 | 257.528 | 199.354 | 273.114 | 199.042 | 199.103 | 171.545 | 94.404 | 95.340 | 167.567 |
| 1 | 20 | 8 | 307.067 | 255.410 | 198.773 | 272.005 | 196.683 | 199.708 | 170.666 | 94.245 | 94.775 | 170.014 |
| 1 | 24 | 8 | 301.156 | 258.092 | 196.917 | 268.972 | 195.562 | 197.487 | 166.793 | 93.954 | 93.843 | 165.076 |
| 1 | 28 | 8 | 317.640 | 264.891 | 204.152 | 278.145 | 204.856 | 205.761 | 175.261 | 96.091 | 97.155 | 172.872 |
| 1 | 32 | 8 | 315.782 | 260.839 | 204.367 | 276.370 | 201.289 | 203.044 | 171.681 | 95.101 | 94.789 | 167.743 |
| 1 | 36 | 8 | 315.484 | 260.754 | 204.294 | 275.794 | 202.039 | 204.046 | 172.066 | 94.366 | 95.812 | 169.300 |
| 1 | 40 | 8 | 317.197 | 265.670 | 204.698 | 276.420 | 202.654 | 205.535 | 172.373 | 96.136 | 95.950 | 168.497 |
| 1 | 44 | 8 | 314.387 | 259.808 | 204.142 | 276.567 | 202.159 | 203.925 | 170.827 | 94.753 | 94.565 | 167.279 |
| 1 | 48 | 8 | 309.150 | 255.109 | 198.860 | 269.221 | 197.116 | 200.271 | 167.568 | 94.141 | 93.967 | 166.421 |
| 1 | 52 | 8 | 292.729 | 242.081 | 188.862 | 257.825 | 187.183 | 189.635 | 160.356 | 90.234 | 89.757 | 158.025 |
| 1 | 56 | 8 | 293.280 | 243.228 | 190.736 | 256.781 | 188.202 | 188.919 | 160.377 | 89.910 | 90.360 | 159.045 |
| 1 | 60 | 8 | 292.197 | 244.585 | 189.041 | 257.525 | 186.637 | 190.583 | 161.049 | 90.028 | 90.828 | 158.581 |

## Prologue-Inclusive Gate

- Gate status: `exact_nonreference_candidates_exist_but_gate_not_met`.
- Rows ready for endpoint gate: `0` / `16`.
- Best exact non-reference full-layerlet candidate: `fused_prologue_middle_layerlet` at `160.356 us` (`1.825x` vs current `xpu_fused_moe`).
- Endpoint promotion allowed by this artifact: `False`.
- Endpoint promotion still requires graph-path tensor capture, accepted-lane quality gates, and a manifest update.

| rows | route start | best exact nonref | best nonref us | speedup vs xpu | target met | status |
|---:|---:|---|---:|---:|---:|---|
| 1 | 0 | fused_prologue_middle_layerlet | 168.158 | 1.853 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 4 | fused_prologue_middle_layerlet | 171.565 | 1.823 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 8 | fused_prologue_middle_layerlet | 177.502 | 1.842 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 12 | fused_prologue_middle_layerlet | 169.926 | 1.829 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 16 | fused_prologue_middle_layerlet | 171.545 | 1.807 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 20 | fused_prologue_middle_layerlet | 170.666 | 1.799 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 24 | fused_prologue_middle_layerlet | 166.793 | 1.806 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 28 | fused_prologue_middle_layerlet | 175.261 | 1.812 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 32 | fused_prologue_middle_layerlet | 171.681 | 1.839 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 36 | fused_prologue_middle_layerlet | 172.066 | 1.834 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 40 | fused_prologue_middle_layerlet | 172.373 | 1.840 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 44 | fused_prologue_middle_layerlet | 170.827 | 1.840 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 48 | fused_prologue_middle_layerlet | 167.568 | 1.845 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 52 | fused_prologue_middle_layerlet | 160.356 | 1.825 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 56 | fused_prologue_middle_layerlet | 160.377 | 1.829 | False | best_exact_nonreference_misses_target_layerlet_us |
| 1 | 60 | fused_prologue_middle_layerlet | 161.049 | 1.814 | False | best_exact_nonreference_misses_target_layerlet_us |

## Decision

- This is a baseline route replay with the current non-fused activation and quantization path.
- The fused-prologue staged path is exact against `xpu_fused_moe` for this route replay.
- The fused-prologue staged path is slower than the simpler preallocated staged path in this full-MoE screen. Do not wire it into the endpoint unless the downstream GEMM ABI can consume prologue offsets directly or the prologue is fused with more downstream work.
- Compare `xpu fused us` with the current budget target of roughly `160 us/layer` for a plausible `200 tok/s` non-speculative lane.
