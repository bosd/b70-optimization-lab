# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-current-eager-tp2-20260617i-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-prefillout-decodestate-eager-tp2-20260617af-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `9`
- Requests: `1`
- Draft tokens: `9`
- Accepted: `8`
- Rejected: `1`
- Accept rate: `88.88888888888889`
- Full accept rows: `8`
- Full reject rows: `1`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `17`
- Accepted token: `321` ` and`
- Candidate token: `11436` ` hardware`
- Accepted window: ` single-request decode speed, reliability gates, and no quality loss.
Continue with speculative`
- Candidate window: ` single-request decode speed, reliability gates, hardware-specific optimizations.

<think>
Thinking Process`
- Replay mapping: `mapped`
  - Request: `cmpl-qwen36-oracle-k1-prefillout-decodestate-eager-tp2-20260617af-000000-0-acda5e5c`
  - Trace row: `9`
  - Position in row: `0`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[321]`
  - Generated: `[11436]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
