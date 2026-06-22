# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-keepcomputed-currentbaseline-eager-tp2-20260617ba-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `2`
- Requests: `1`
- Draft tokens: `2`
- Accepted: `1`
- Rejected: `1`
- Accept rate: `50.0`
- Full accept rows: `1`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `2`
- Accepted token: `27044` ` dense`
- Candidate token: `14246` ` engineering`
- Accepted window: `Continue with dense numbered engineering notes. Focus on single-request`
- Candidate window: `Continue with engineering notes. Focus on single-request decode speed`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
