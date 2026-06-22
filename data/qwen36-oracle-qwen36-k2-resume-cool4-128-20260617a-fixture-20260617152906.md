# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-smallcap-current-candidate-20260615nospecsmall1.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k2-resume-cool4-128-candidate-20260617a.json`
- Exact match all: `False`
- Mismatches: `2` / `2`

## Scheduler Summary

- Rows: `12`
- Requests: `2`
- Draft tokens: `24`
- Accepted: `21`
- Rejected: `3`
- Accept rate: `87.5`
- Full accept rows: `9`
- Full reject rows: `0`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `28`
- Accepted token: `90700` `Thinking`
- Candidate token: `8160` `Here`
- Accepted window: ` and no quality loss.

<think>
Thinking Process:

1.  **De`
- Candidate window: ` and no quality loss.

<think>
Here's a thinking thinking sequence

1.`
- Replay mapping: `trace_emitted_sequence_not_found_in_candidate`

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
- Replay mapping: `trace_emitted_sequence_not_found_in_candidate`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
