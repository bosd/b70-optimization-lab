# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-smallcap-micro-candidate-20260616micro1.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-targetowned-adraftfix-smallgraph-candidate-20260617a.json`
- Exact match all: `False`
- Mismatches: `1` / `2`

## Scheduler Summary

- Rows: `4`
- Requests: `2`
- Draft tokens: `4`
- Accepted: `2`
- Rejected: `2`
- Accept rate: `50.0`
- Full accept rows: `2`
- Full reject rows: `2`

## Case Diffs

### natural_latency_plan

- Status: `match`
- First diff: none

### repetitive_kernel_notes

- Status: `mismatch`
- First diff index: `14`
- Accepted token: `6126` `PU`
- Candidate token: `271` `

`
- Accepted window: ` while measuring multi token verification. Intel XPU decode verifier bucket route

<think>

</think>`
- Candidate window: ` while measuring multi token verification. Intel X

<think>

</think>

Intel XPU decode`
- Replay mapping: `trace_emitted_sequence_not_found_in_candidate`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
