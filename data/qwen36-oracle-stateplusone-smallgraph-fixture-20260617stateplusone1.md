# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-smallcap-micro-candidate-20260616micro1.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-stateplusone-smallgraph-candidate-20260617a.json`
- Exact match all: `False`
- Mismatches: `1` / `2`

## Scheduler Summary

- Rows: `29`
- Requests: `2`
- Draft tokens: `29`
- Accepted: `27`
- Rejected: `2`
- Accept rate: `93.10344827586206`
- Full accept rows: `27`
- Full reject rows: `2`

## Case Diffs

### natural_latency_plan

- Status: `match`
- First diff: none

### repetitive_kernel_notes

- Status: `mismatch`
- First diff index: `19`
- Accepted token: `271` `

`
- Candidate token: `4618` ` graph`
- Accepted window: `. Intel XPU decode verifier bucket route

<think>

</think>

Intel XPU decode`
- Candidate window: `. Intel XPU decode verifier bucket route graph token timing. Preserve exact output while measuring`
- Replay mapping: `mapped`
  - Request: `cmpl-stateplusone20260617a-000001-0-814b8dfe`
  - Trace row: `29`
  - Position in row: `0`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[271]`
  - Generated: `[4618]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
