# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-promote-default-currentbaseline-eager-tp2-20260617bf-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `1`
- Requests: `1`
- Draft tokens: `1`
- Accepted: `1`
- Rejected: `0`
- Accept rate: `100.0`
- Full accept rows: `1`
- Full reject rows: `0`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `2`
- Accepted token: `27044` ` dense`
- Candidate token: `874` ` no`
- Accepted window: `Continue with dense numbered engineering notes. Focus on single-request`
- Candidate window: `Continue with no quality loss.

<think>
Thinking Process`
- Replay mapping: `first_diff_outside_trace_emitted_sequence`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
