# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-commitfull-placeholder-20260618b-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `2`
- Requests: `1`
- Draft tokens: `16`
- Accepted: `15`
- Rejected: `1`
- Accept rate: `93.75`
- Full accept rows: `1`
- Full reject rows: `0`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `9`
- Accepted token: `3074` ` single`
- Candidate token: `43318` `-request`
- Accepted window: ` with dense numbered engineering notes. Focus on single-request decode speed, reliability gates, and`
- Candidate window: ` with dense numbered engineering notes. Focus on-request decode speed, reliability gates, and no`
- Replay mapping: `mapped`
  - Request: `cmpl-qwen36-oracle-k8-draftonly-piecewise-skipcompiledspec-commitfull-placeholder-20260618b-000000-0-901be818`
  - Trace row: `2`
  - Position in row: `0`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[3074, 43318, 16401, 4478, 11, 29541, 33389, 11]`
  - Generated: `[43318, 16401, 4478, 11, 29541, 33389, 11]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
