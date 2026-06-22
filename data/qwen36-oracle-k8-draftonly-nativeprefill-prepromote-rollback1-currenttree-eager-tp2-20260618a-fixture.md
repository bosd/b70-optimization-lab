# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-nativeprefill-prepromote-rollback1-currenttree-eager-tp2-20260618a-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `2`
- Requests: `1`
- Draft tokens: `16`
- Accepted: `8`
- Rejected: `8`
- Accept rate: `50.0`
- Full accept rows: `1`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `17`
- Accepted token: `321` ` and`
- Candidate token: `11436` ` hardware`
- Accepted window: ` single-request decode speed, reliability gates, and no quality loss.

<think>

</think>`
- Candidate window: ` single-request decode speed, reliability gates, hardware acceleration, and no quality loss.
`
- Replay mapping: `first_diff_outside_trace_emitted_sequence`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
