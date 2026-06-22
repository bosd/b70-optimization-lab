# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `14`
- Requests: `1`
- Draft tokens: `14`
- Accepted: `9`
- Rejected: `5`
- Accept rate: `64.28571428571429`
- Full accept rows: `9`
- Full reject rows: `5`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `23`
- Accepted token: `248068` `<think>`
- Candidate token: `248046` `<|im_end|>`
- Accepted window: ` gates, and no quality loss.

<think>

</think>

1. **Graph Capture`
- Candidate window: ` gates, and no quality loss.

<|im_end|>`
- Replay mapping: `trace_emitted_sequence_not_found_in_candidate`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
