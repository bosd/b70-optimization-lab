# Qwen3.6 Oracle k=1 Drift Fixture

- Accepted: `/home/steve/llm-optimizations/data/qwen36-nospec-notrace-fixture-eager-tp2-20260617ao-candidate.json`
- Candidate: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-draftonly-serialgdnpacked-promoteconv-commitstate-tailfallback-currentbaseline-eager-tp2-20260618cd-candidate.json`
- Exact match all: `False`
- Mismatches: `1` / `1`

## Scheduler Summary

- Rows: `1`
- Requests: `1`
- Draft tokens: `8`
- Accepted: `7`
- Rejected: `1`
- Accept rate: `87.5`
- Full accept rows: `0`
- Full reject rows: `0`

## Case Diffs

### natural_latency_plan

- Status: `mismatch`
- First diff index: `1`
- Accepted token: `440` ` with`
- Candidate token: `27044` ` dense`
- Accepted window: `Continue with dense numbered engineering notes. Focus on single`
- Candidate window: `Continue dense numbered engineering notes. Focus on single-request`
- Replay mapping: `mapped`
  - Request: `cmpl-qwen36-oracle-k8-draftonly-serialgdnpacked-promoteconv-commitstate-tailfallback-currentbaseline-eager-tp2-20260618cd-000000-0-90204098`
  - Trace row: `1`
  - Position in row: `0`
  - Emission role: `replacement_after_reject`
  - Scheduled: `[440, 27044, 47193, 14246, 8129, 13, 24985, 383]`
  - Generated: `[27044, 47193, 14246, 8129, 13, 24985, 383]`

## Next Actions

- Use this fixture as the token-parity gate for any speculative scheduler/KV patch.
- First repair k=1 oracle parity before enabling DFlash, MTP, n-gram, or learned proposers.
- If a patch passes this fixture, rerun full r8 quality through the paused-local public frontdoor.
