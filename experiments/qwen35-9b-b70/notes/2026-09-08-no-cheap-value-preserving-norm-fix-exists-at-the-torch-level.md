# There is no cheap value-preserving norm fix at the PyTorch level

## What was being looked for

The RMSNorm on Qwen3.5's serving path is row-count dependent, and a float16 reformulation is
invariant but changes values, so adopting it would invalidate every published hash. This went after
the version that would not: something invariant *and* bit-identical to the current op at one row.

That target is the right one because of how the gates work. Exactly preserving the current op at
every row count is impossible - it already disagrees with itself across row counts, which is the
bug. But the identity ladders compare a batch against a sequential oracle, and that oracle runs one
row at a time. A replacement that is row-invariant and equal to native at M=1 would make every batch
reproduce the published oracle, closing the ladders with no re-qualification at all.

The search is cheap because the native op turns out to be **pure PyTorch**, not a custom kernel:

```python
x = x.to(torch.float32)
variance = x.pow(2).mean(dim=-1, keepdim=True)
x = x * torch.rsqrt(variance + epsilon)
x = x.to(weight.dtype) * weight
```

So the shape dependence is in `torch.mean(dim=-1)` over a float32 tensor, and any fix is a Python
change needing no oneDNN rebuild.

## Reformulating the reduction does not help

Four ways of forming the same sum, five seeds, hidden 4096. All four agree with native at M=1, and
none is invariant:

| formulation | rows differing from its own M=1 |
| --- | ---: |
| `x2.mean(-1)` (native) | 27/1250 |
| `x2.sum(-1) / N` | 27/1250 |
| `x2.unsqueeze(1).sum(-1).squeeze(1) / N` | 27/1250 |
| `(x2 @ ones) / N` | 52/1250 |

Sum, mean and the unsqueeze folding are bit-identical to each other at every row count, so they
funnel into the same reduction kernel; the matmul formulation is a different kernel and is worse.
The dependence is inside PyTorch's float32 reduction, not in how the expression is written.

## Chunking does not preserve the oracle either, and the reason I thought it might was a sampling artifact

The per-row-count data above looked like it contained a lever: at 2 and 8 rows it showed **zero**
differences, with the dependence only appearing from 16 up. If that held, reducing in fixed chunks of
8 would reproduce the M=1 oracle at a sixteenth of the launches of row-at-a-time.

It does not hold. Re-measured against the native M=1 oracle with eight seeds instead of five:

| chunk | rows differing from native at M=1 | us/forward at 128 rows |
| ---: | ---: | ---: |
| 1 | **0/1920** | `1289.0` |
| 2 | 30/1920 | `666.7` |
| 4 | 42/1920 | `355.4` |
| 8 | 35/1920 | `192.7` |
| 16 | 40/1920 | `114.6` |
| 32 | 51/1920 | `74.8` |
| unchunked | 51/1920 | `39.0` |

Only chunk size 1 preserves the oracle. The `{2: 0, 8: 0}` that suggested otherwise was five seeds
being lucky; with eight, two-row and eight-row reductions both differ from one-row reductions,
just rarely. That is the third small-sample pattern to dissolve under more sampling today, after the
norm's apparent clean threshold at 32 rows and the Gemma draft-thread win.

One thing the table does refine usefully: an oracle-preserving reduction costs about **33x**
(`1289` against `39 us`), not the 108x the earlier whole-norm row-at-a-time measurement suggested,
because only the variance reduction has to be serialised, not the whole norm. Both figures are
launch-overhead dominated at this size, so treat the ratio as the meaningful part.

## What this closes, and what is left

Closed: there is no cheap, value-preserving fix available by rewriting the reduction in PyTorch.
Anyone who wants one has exactly three options, and none is free.

1. **Serialise the variance reduction.** Preserves every published oracle output, needs no
   re-qualification, costs about 33x on the norm. Whether that is tolerable end to end is a
   measurement nobody has taken - the norms' share of decode time on this model is unknown, and that
   is the cheapest next thing to find out.
2. **Switch to the float16 reduction.** Invariant and not obviously more expensive, but a different
   rounding: changes outputs, invalidates every hash, requires re-running the whole identity chain.
3. **Write an actually-invariant kernel.** The only option that is both cheap and value-preserving,
   and the only one that is real work rather than a configuration choice.

Before any of them, the useful measurement is option 1's end-to-end cost, because it is the only one
that can be tried without regenerating the lane's evidence.

Evidence: `data/2026-09-08-rmsnorm-reduction-candidates.json`,
`data/2026-09-08-rmsnorm-chunked-reduction.json`; probes
`probes/rmsnorm-reduction-candidates.py`, `probes/rmsnorm-chunked-reduction.py`.
