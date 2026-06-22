# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-dflash-k15-eager-tp2-recover-replacement-20260619a-20260619dflashrecover1-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `4`
- Requests: `1`
- Draft tokens: `60`
- Accepted: `7`
- Rejected: `53`
- Accept rate: `11.666666666666666`
- Full accept rows: `0`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `2`
- Accepted token: `27044` ` dense`
- Candidate token: `440` ` with`
- Accepted window: `Continue with dense numbered engineering notes. Focus on single-request`
- Candidate window: `Continue with with dense numbered engineering notes. Focus on single`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
