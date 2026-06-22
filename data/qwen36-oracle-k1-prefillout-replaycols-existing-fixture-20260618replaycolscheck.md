# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-current-eager-tp2-20260617i-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-prefillout-replaycols-eager-tp2-20260617ag-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `4`
- Requests: `1`
- Draft tokens: `4`
- Accepted: `3`
- Rejected: `1`
- Accept rate: `75.0`
- Full accept rows: `3`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `7`
- Accepted token: `24985` ` Focus`
- Candidate token: `271` `

`
- Accepted window: `Continue with dense numbered engineering notes. Focus on single-request decode speed, reliability gates`
- Candidate window: `Continue with dense numbered engineering notes.

<think>
Thinking Process:

1.`
- Replay mapping: `mapped`
  - Request: `cmpl-qwen36-oracle-k1-prefillout-replaycols-eager-tp2-20260617ag-000000-0-bed8a690`
  - Trace row: `4`
  - Position in row: `0`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[24985]`
  - Generated: `[271]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
