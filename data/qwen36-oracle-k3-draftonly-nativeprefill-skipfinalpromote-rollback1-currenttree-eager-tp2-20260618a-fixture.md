# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k3-draftonly-nativeprefill-skipfinalpromote-rollback1-currenttree-eager-tp2-20260618a-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `3`
- Requests: `1`
- Draft tokens: `9`
- Accepted: `6`
- Rejected: `3`
- Accept rate: `66.66666666666667`
- Full accept rows: `2`
- Full reject rows: `1`

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
- Replay mapping: `first_diff_outside_trace_emitted_sequence`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
