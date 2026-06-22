# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-serialgdn-nopostprocess-control-currenttree-eager-tp2-20260618b-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `4`
- Requests: `1`
- Draft tokens: `32`
- Accepted: `16`
- Rejected: `16`
- Accept rate: `50.0`
- Full accept rows: `2`
- Full reject rows: `2`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `18`
- Accepted token: `874` ` no`
- Candidate token: `11` `,`
- Accepted window: `-request decode speed, reliability gates, and no quality loss.

<think>

</think>

`
- Candidate window: `-request decode speed, reliability gates, and, and, and, and, and,`
- Replay mapping: `trace_emitted_sequence_not_found_in_candidate`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
