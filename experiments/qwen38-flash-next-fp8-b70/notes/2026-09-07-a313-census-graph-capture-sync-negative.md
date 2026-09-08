# A313 (negative): a data-dependent shape in an instrumentation hook aborts graph capture

**What happened.** A313 extended the placement census from "how many parked experts were
selected" to a full per-expert histogram, by masking the routed ids and counting them:

```python
sel = torch.where(valid, ids, torch.full_like(ids, -1))
sel = sel[sel >= 0]                      # <- data-dependent shape
counts += torch.bincount(sel, minlength=counts.numel())
```

The server never became healthy. The workers died during `compile_or_warm_up_model` with

```
RuntimeError: Worker failed with error 'wait method cannot be used for an event
associated with a command graph.'
```

**Why.** `sel[sel >= 0]` is a boolean mask index. Its output shape depends on the values in
`sel`, so the runtime must read the mask back to the host to size the result — a
synchronisation, on every launch. Inside XPU graph capture a synchronisation is illegal,
and the worker aborts rather than degrade.

**The fix, and why the earlier census survived.** A `scatter_add_` with a zero weight for
invalid slots is statically shaped and needs no sync:

```python
counts.scatter_add_(0, ids.clamp_min(0).reshape(-1), valid.reshape(-1).to(torch.int64))
```

A311's census ran under the same capture because it only did `mask[ids] & valid` and two
`.sum()` accumulations into a device tensor — every shape static. The sync arrived with the
histogram, not with the instrumentation as such.

**The general rule.** This is the third instrumentation-versus-capture failure on this lane,
after the MoE event-timing hooks (A283) and the profiler's own overhead. An instrumentation
hook that runs inside the captured region must be static in shape and must not read a
device value back to the host. Counting is fine; deciding how much to count is not.

Nothing about the model or the placement hypothesis is implicated: A313 never served a
token. A315 repeats it on the graph-safe head `cc653214`.

## Evidence

- `data/20260907-tp4-mtp1-a313-graph-capture-sync-abort.log` — the abort and its stack.
- Packet: `tools/rewrite-q38-a311-to-a313-mtp1-placement-routing-census.py`; overlay head
  `c3b044c1` (the syncing version, kept so the negative can be reproduced).
