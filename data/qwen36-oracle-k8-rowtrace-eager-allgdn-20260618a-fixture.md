# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-rowtrace-eager-allgdn-20260618a-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `3`
- Requests: `1`
- Draft tokens: `24`
- Accepted: `24`
- Rejected: `0`
- Accept rate: `100.0`
- Full accept rows: `3`
- Full reject rows: `0`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `26`
- Accepted token: `271` `

`
- Candidate token: `None` `None`
- Accepted window: ` no quality loss.

<think>

</think>

1. **Graph Capture`
- Candidate window: ` no quality loss.

<think>

</think>`
- Replay mapping: `first_diff_outside_trace_emitted_sequence`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
