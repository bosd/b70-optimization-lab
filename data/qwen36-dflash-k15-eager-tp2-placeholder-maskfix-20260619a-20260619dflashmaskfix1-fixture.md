# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-dflash-k15-eager-tp2-placeholder-maskfix-20260619a-20260619dflashmaskfix1-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `6`
- Requests: `1`
- Draft tokens: `90`
- Accepted: `35`
- Rejected: `55`
- Accept rate: `38.888888888888886`
- Full accept rows: `1`
- Full reject rows: `2`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `24`
- Accepted token: `271` `

`
- Candidate token: `198` `
`
- Accepted window: `, and no quality loss.

<think>

</think>

1. **Graph Capture`
- Candidate window: `, and no quality loss.

<think>
Thinking Process:

1. `
- Replay mapping: `mapped`
  - Request: `cmpl-qwen36-dflash-k15-eager-tp2-placeholder-maskfix-20260619a-20260619dflashmaskfix1-000000-0-85dc4c39`
  - Trace row: `4`
  - Position in row: `0`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]`
  - Generated: `[198]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
