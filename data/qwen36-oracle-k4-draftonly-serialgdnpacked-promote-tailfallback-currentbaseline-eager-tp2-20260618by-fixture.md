# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k4-draftonly-serialgdnpacked-promote-tailfallback-currentbaseline-eager-tp2-20260618by-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `7`
- Requests: `1`
- Draft tokens: `28`
- Accepted: `28`
- Rejected: `0`
- Accept rate: `100.0`
- Full accept rows: `7`
- Full reject rows: `0`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `29`
- Accepted token: `2972` ` **`
- Candidate token: `271` `

`
- Accepted window: `.

<think>

</think>

1. **Graph Capture`
- Candidate window: `.

<think>

</think>

1.

1.`
- Replay mapping: `first_diff_outside_trace_emitted_sequence`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
