# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `7`
- Requests: `1`
- Draft tokens: `105`
- Accepted: `27`
- Rejected: `78`
- Accept rate: `25.714285714285715`
- Full accept rows: `0`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `25`
- Accepted token: `248069` `</think>`
- Candidate token: `8160` `Here`
- Accepted window: ` and no quality loss.

<think>

</think>

1. **Graph Capture`
- Candidate window: ` and no quality loss.

<think>

Here is a technical latency plan for`
- Replay mapping: `mapped`
  - Request: `cmpl-qwen36-dflash-k15-eager-tp2-serial-gdn-sync-20260619a-20260619dflashserial1-000000-0-82dee3e3`
  - Trace row: `5`
  - Position in row: `0`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[8160, 579, 264, 7047, 1817, 25, 271, 16, 13, 220, 2972, 1847, 7355, 279, 5396]`
  - Generated: `[8160, 369]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
