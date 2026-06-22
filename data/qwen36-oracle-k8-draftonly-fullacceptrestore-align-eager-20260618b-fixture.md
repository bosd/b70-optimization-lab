# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618b-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `1`
- Requests: `1`
- Draft tokens: `8`
- Accepted: `8`
- Rejected: `0`
- Accept rate: `100.0`
- Full accept rows: `1`
- Full reject rows: `0`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `9`
- Accepted token: `3074` ` single`
- Candidate token: `440` ` with`
- Accepted window: ` with dense numbered engineering notes. Focus on single-request decode speed, reliability gates, and`
- Candidate window: ` with dense numbered engineering notes. Focus on with dense numbered engineering notes. Focus on

`
- Replay mapping: `first_diff_outside_trace_emitted_sequence`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
