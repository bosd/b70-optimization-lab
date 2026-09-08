# The QSA selection sort is launch-bound, so the algorithmic lever is dead

**The target.** With the MoE tile question closed, QSA is the largest untouched block of the
decode step. Its XPU selection is a full stable argsort followed by a slice:

```python
ranked = torch.argsort(logits, dim=1, descending=True, stable=True)[:, :block_topk]
```

The source comment explains the choice: the generic XPU top-k resolves ties by atomic
reservation order, so both the order and the selected set can vary between identical
launches, and QSA consumes the order directly — so the order is load-bearing for exactness
and cannot be dropped. A full sort where a top-k would do is the classic overpay, so it
looked like a lever.

**The shapes.** `indexer_budget` 2048, `indexer_compress_ratio` 4. At the benchmark's
2048-token depth, 512 blocks are visible and all 512 are kept: the sort buys *ordering only*,
no selection at all. At 4096, 1024 are visible and 512 kept, so k is half of n — already a
regime where top-k saves little.

**The measurement** (isolated, per call, k = 512):

| rows × cols | stable argsort | `topk(sorted=True)` | `sort` values | × 48 layers |
| --- | --- | --- | --- | --- |
| 1 × 512 | 23.5 µs | 28.3 µs | 23.4 µs | **1.13 ms** |
| 1 × 1024 | 24.1 µs | 29.8 µs | 24.0 µs | 1.16 ms |
| 1 × 2048 | 30.3 µs | 33.0 µs | 30.0 µs | 1.46 ms |
| 4 × 512 | 23.2 µs | 28.8 µs | 23.1 µs | 1.11 ms |

**Two results, both negative for the obvious plan.**

`torch.topk(sorted=True)` is *slower* than the full stable argsort at every shape measured,
by 20–25%. The cheaper-looking algorithm is a regression, quite apart from its tie-order
nondeterminism.

And the cost is nearly flat in n: quadrupling the sorted length from 512 to 2048 costs 29%
more time, not 4x. The op is launch- and latency-bound at these sizes, not work-bound. That
kills the algorithmic lever outright — you cannot win by sorting less when sorting is not
what is being paid for.

**What the opportunity actually is.** About 1.13 ms per step at the 2K depth against a
~29.9 ms step (34.5 tok/s), so ~3.8%, and it is a *launch*. The only way to collect it is to
remove the launch — fuse the selection into an adjacent kernel — while reproducing
score-desc / logical-index-asc order exactly. That is a real kernel-writing project with an
exactness obligation, worth at most ~1.3 tok/s if fusion were free, and it should be costed
against the MoE dependency chain before either is started.

**Caveats.** These are isolated timings; the ranking of *kernel variants* on this machine has
to happen in the server (A320, A327). What the isolated harness is being used for here is an
order-of-magnitude cost for a single torch op and the shape of its scaling curve, which is
much weaker a claim than a tile ranking. The 48x multiplier assumes one selection per layer
per step.

## Evidence

- `tools/probe-qsa-selection-argsort-offline.py` — the table above.
- Selection source: `vllm/models/qwen4_exp/amd/ops/qsa.py` at overlay head `2a372e86`.
- Shapes: `text_config.indexer_budget` 2048, `indexer_compress_ratio` 4.
