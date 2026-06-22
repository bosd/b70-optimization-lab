# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-graph-tp2-replayaccepted-skippost-20260618d-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `2`
- Requests: `1`
- Draft tokens: `16`
- Accepted: `15`
- Rejected: `1`
- Accept rate: `93.75`
- Full accept rows: `1`
- Full reject rows: `0`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `17`
- Accepted token: `321` ` and`
- Candidate token: `11436` ` hardware`
- Accepted window: ` single-request decode speed, reliability gates, and no quality loss.

<think>

</think>`
- Candidate window: ` single-request decode speed, reliability gates, hardware-specific tuning.

<think>
Thinking Process`
- Replay mapping: `mapped`
  - Request: `cmpl-qwen36-oracle-k8-graph-tp2-replayaccepted-skippost-20260618d-000000-0-809dd267`
  - Trace row: `2`
  - Position in row: `7`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[43318, 16401, 4478, 11, 29541, 33389, 11, 321]`
  - Generated: `[43318, 16401, 4478, 11, 29541, 33389, 11, 11436]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
