# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-serialgdnpacked-preemptbonus-currentbaseline-eager-tp2-20260618bs-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `6`
- Requests: `1`
- Draft tokens: `6`
- Accepted: `6`
- Rejected: `0`
- Accept rate: `100.0`
- Full accept rows: `6`
- Full reject rows: `0`

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
- Replay mapping: `trace_emitted_sequence_not_found_in_candidate`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
