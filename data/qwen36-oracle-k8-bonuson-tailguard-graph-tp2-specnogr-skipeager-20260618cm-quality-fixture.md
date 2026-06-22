# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-bonuson-tailguard-graph-tp2-specnogr-skipeager-20260618cm-quality.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `3`
- Requests: `1`
- Draft tokens: `24`
- Accepted: `19`
- Rejected: `5`
- Accept rate: `79.16666666666667`
- Full accept rows: `2`
- Full reject rows: `0`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `22`
- Accepted token: `271` `

`
- Candidate token: `198` `
`
- Accepted window: ` reliability gates, and no quality loss.

<think>

</think>

1. **Graph`
- Candidate window: ` reliability gates, and no quality loss.
Continue with dense numbered engineering notes.

`
- Replay mapping: `mapped`
  - Request: `cmpl-qwen36-oracle-k8-bonuson-tailguard-graph-tp2-specnogr-skipeager-20260618cm-quality-000000-0-bd7bbcc7`
  - Trace row: `3`
  - Position in row: `3`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[4131, 4557, 13, 271, 248068, 271, 248069, 271]`
  - Generated: `[4131, 4557, 13, 198]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
