# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-smallcap-micro-candidate-20260616micro1.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-serialconv-smallgraph-candidate-20260617c.json`
- Exact match all: `False`
- Mismatches: `2` / `2`

## Scheduler Summary

- Rows: `31`
- Requests: `2`
- Draft tokens: `31`
- Accepted: `30`
- Rejected: `1`
- Accept rate: `96.7741935483871`
- Full accept rows: `30`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `18`
- Accepted token: `29796` ` acceleration`
- Candidate token: `11` `,`
- Accepted window: `-request decode speed, reliability gates, hardware acceleration, and no quality loss.

<think>`
- Candidate window: `-request decode speed, reliability gates, hardware, and no quality loss.
Continue with`
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
- Replay mapping: `mapped`
  - Request: `cmpl-serialconv-c-000001-0-816c9d7f`
  - Trace row: `25`
  - Position in row: `0`
  - Emission role: `accepted_draft`
  - Scheduled: `[4618]`
  - Generated: `[4618, 3817]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
