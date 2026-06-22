# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-dflash-k15-eager-tp2-no-preempt-replacement-20260619b-20260619dflashnopreempt2-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `7`
- Requests: `1`
- Draft tokens: `105`
- Accepted: `34`
- Rejected: `71`
- Accept rate: `32.38095238095238`
- Full accept rows: `0`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `4`
- Accepted token: `14246` ` engineering`
- Candidate token: `440` ` with`
- Accepted window: `Continue with dense numbered engineering notes. Focus on single-request decode speed`
- Candidate window: `Continue with dense numbered with dense numbered engineering notes. Focus on single`
- Replay mapping: `trace_emitted_sequence_not_found_in_candidate`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
