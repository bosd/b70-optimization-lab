# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-fullacceptrestore-align-eager-20260618c-candidate.json`
- Exact match all: `True`
- Mismatches: `0` / `1`

## Scheduler Summary

- Rows: `4`
- Requests: `1`
- Draft tokens: `32`
- Accepted: `22`
- Rejected: `10`
- Accept rate: `68.75`
- Full accept rows: `2`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `match`
- First diff: none

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
