# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-draftonly-currentbaseline-eager-tp2-20260618bu-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `17`
- Requests: `1`
- Draft tokens: `17`
- Accepted: `16`
- Rejected: `1`
- Accept rate: `94.11764705882354`
- Full accept rows: `16`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `17`
- Accepted token: `321` ` and`
- Candidate token: `343` ` v`
- Accepted window: ` single-request decode speed, reliability gates, and no quality loss.

<think>

</think>`
- Candidate window: ` single-request decode speed, reliability gates, vLLM XPU, tensor parallelism`
- Replay mapping: `first_diff_outside_trace_emitted_sequence`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
