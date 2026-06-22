# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-smallcap-current-candidate-20260615nospecsmall1.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k2-resume-nobonus128-candidate-20260617a.json`
- Exact match all: `False`
- Mismatches: `2` / `2`

## Scheduler Summary

- Rows: `28`
- Requests: `2`
- Draft tokens: `56`
- Accepted: `51`
- Rejected: `5`
- Accept rate: `91.07142857142857`
- Full accept rows: `25`
- Full reject rows: `2`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `14`
- Accepted token: `29541` ` reliability`
- Candidate token: `4779` ` memory`
- Accepted window: `. Focus on single-request decode speed, reliability gates, hardware acceleration, and no quality`
- Candidate window: `. Focus on single-request decode speed, memory management, and no quality loss.
`

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
- Candidate window: `. Intel XPU decode verifier bucket route graph token timing. Preserve exact input while measuring`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
