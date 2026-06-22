# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-think-bonus-force-single-20260618h-candidate.json`
- Exact match all: `True`
- Mismatches: `0` / `1`

## Scheduler Summary

- Rows: `16`
- Requests: `1`
- Draft tokens: `16`
- Accepted: `15`
- Rejected: `1`
- Accept rate: `93.75`
- Full accept rows: `15`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `match`
- First diff: none

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
