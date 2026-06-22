# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-draftonly-serialgdnpacked-currentbaseline-eager-tp2-20260618bt-candidate.json`
- Exact match all: `True`
- Mismatches: `0` / `1`

## Scheduler Summary

- Rows: `31`
- Requests: `1`
- Draft tokens: `31`
- Accepted: `31`
- Rejected: `0`
- Accept rate: `100.0`
- Full accept rows: `31`
- Full reject rows: `0`

## Case Diffs

### natural_latency_plan

- Status: `match`
- First diff: none

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
