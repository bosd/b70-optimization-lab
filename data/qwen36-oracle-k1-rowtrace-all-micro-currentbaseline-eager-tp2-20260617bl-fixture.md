# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-rowtrace-all-micro-currentbaseline-eager-tp2-20260617bl-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `13`
- Requests: `1`
- Draft tokens: `13`
- Accepted: `11`
- Rejected: `2`
- Accept rate: `84.61538461538461`
- Full accept rows: `11`
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
- Replay mapping: `trace_emitted_sequence_not_found_in_candidate`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
