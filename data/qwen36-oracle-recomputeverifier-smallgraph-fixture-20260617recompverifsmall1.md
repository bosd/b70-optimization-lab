# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-smallcap-micro-candidate-20260616micro1.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-recomputeverifier-smallgraph-candidate-20260617a.json`
- Exact match all: `False`
- Mismatches: `2` / `2`

## Scheduler Summary

- Rows: `2`
- Requests: `2`
- Draft tokens: `2`
- Accepted: `2`
- Rejected: `0`
- Accept rate: `100.0`
- Full accept rows: `2`
- Full reject rows: `0`

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
- Replay mapping: `first_diff_outside_trace_emitted_sequence`

### repetitive_kernel_notes

- Status: `mismatch`
- First diff index: `15`
- Accepted token: `16401` ` decode`
- Candidate token: `17120` ` architecture`
- Accepted window: ` measuring multi token verification. Intel XPU decode verifier bucket route

<think>

</think>

`
- Candidate window: ` measuring multi token verification. Intel XPU architecture.

<think>
Here's a thinking`
- Replay mapping: `first_diff_outside_trace_emitted_sequence`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
