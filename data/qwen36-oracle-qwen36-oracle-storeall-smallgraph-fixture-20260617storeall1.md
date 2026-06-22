# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-smallcap-micro-candidate-20260616micro1.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-storeall-smallgraph-candidate-20260617a.json`
- Exact match all: `False`
- Mismatches: `2` / `2`

## Scheduler Summary

- Rows: `19`
- Requests: `2`
- Draft tokens: `19`
- Accepted: `17`
- Rejected: `2`
- Accept rate: `89.47368421052632`
- Full accept rows: `17`
- Full reject rows: `2`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `17`
- Accepted token: `11436` ` hardware`
- Candidate token: `4779` ` memory`
- Accepted window: ` single-request decode speed, reliability gates, hardware acceleration, and no quality loss.

`
- Candidate window: ` single-request decode speed, reliability gates, memory management, and no quality loss.
`
- Replay mapping: `mapped`
  - Request: `cmpl-storeall20260617a-000000-0-a5a3c50b`
  - Trace row: `9`
  - Position in row: `0`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[11436]`
  - Generated: `[4779]`

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
  - Request: `cmpl-storeall20260617a-000001-0-a9f172f9`
  - Trace row: `19`
  - Position in row: `0`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[271]`
  - Generated: `[4618]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
