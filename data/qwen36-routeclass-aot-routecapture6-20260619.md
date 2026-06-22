# Qwen3.6 Route-Class AOT Plan

- Status: `needs_more_route_windows_before_aot_commit`.
- Records used: `285` / `285`.
- Fixture events: `0`.
- Layers: `3`.
- Global unique route classes: `285`.
- Per-layer exact route classes: `285` (mean `95.000` per layer).
- Exact unique hot-pack memory for seen layers: `270.129 MiB` per TP shard.
- Exact hot-pack fraction of full seen-layer MoE shards: `0.464`.

## Budget Coverage

| classes/layer | mean coverage | min coverage | unique hot-pack MiB | duplicate route-pack MiB |
|---:|---:|---:|---:|---:|
| 1 | 0.011 | 0.011 | 18.211 | 18.211 |
| 2 | 0.021 | 0.021 | 30.352 | 36.422 |
| 4 | 0.042 | 0.042 | 55.392 | 72.844 |
| 8 | 0.084 | 0.084 | 75.120 | 145.688 |
| 16 | 0.168 | 0.168 | 100.919 | 291.375 |
| 32 | 0.337 | 0.337 | 154.034 | 582.750 |

## Top Global Route Classes

- `f740ff70056d1a03` count `1`, coverage `0.004`, topk `[59, 2, 243, 161, 255, 170, 200, 36]`
- `77d1575c2d379531` count `1`, coverage `0.004`, topk `[137, 32, 189, 88, 103, 64, 125, 148]`
- `733da171d0660cf6` count `1`, coverage `0.004`, topk `[156, 243, 2, 197, 239, 170, 26, 148]`
- `8d30131e0b8ced63` count `1`, coverage `0.004`, topk `[59, 156, 200, 243, 197, 255, 170, 171]`
- `4a3c37d35a36d558` count `1`, coverage `0.004`, topk `[71, 230, 191, 103, 177, 41, 236, 57]`
- `de290f7abbf38d70` count `1`, coverage `0.004`, topk `[18, 194, 246, 45, 156, 243, 127, 201]`
- `b4400be983a87dde` count `1`, coverage `0.004`, topk `[61, 166, 251, 243, 250, 42, 95, 188]`
- `990d6729feeffe7e` count `1`, coverage `0.004`, topk `[194, 96, 182, 183, 64, 175, 138, 214]`

## Layer Snapshot

| layer | records | unique classes | top1 coverage | top2 coverage | top3 coverage |
|---|---:|---:|---:|---:|---:|
| language_model.model.layers.14.mlp.experts | 95 | 95 | 0.011 | 0.021 | n/a |
| language_model.model.layers.21.mlp.experts | 95 | 95 | 0.011 | 0.021 | n/a |
| language_model.model.layers.9.mlp.experts | 95 | 95 | 0.011 | 0.021 | n/a |

## Interpretation

This is an AOT planning gate only. It estimates route-class coverage and hot-pack memory from captured routes; it does not prove speed or quality. Kernel candidates still need graph-path tensor parity, prologue-inclusive timing, quality gates, and an accepted-lane manifest before endpoint promotion.
