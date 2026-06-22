# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-graph-tp2-replayaccepted-multislot-neutral-eager-20260618i-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `4`
- Requests: `1`
- Draft tokens: `32`
- Accepted: `19`
- Rejected: `13`
- Accept rate: `59.375`
- Full accept rows: `2`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `23`
- Accepted token: `248068` `<think>`
- Candidate token: `16` `1`
- Accepted window: ` gates, and no quality loss.

<think>

</think>

1. **Graph Capture`
- Candidate window: ` gates, and no quality loss.

1. **Kernel Fusion & Graph Capture Optimization`
- Replay mapping: `first_diff_outside_trace_emitted_sequence`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
