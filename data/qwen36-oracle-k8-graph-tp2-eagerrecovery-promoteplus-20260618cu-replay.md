# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k8-graph-tp2-eagerrecovery-promoteplus-20260618cu-spec-trace.jsonl`
- rows: `4`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-graph-tp2-eagerrecovery-promoteplus-20260618cu-000000-0-872a9442` | 4 | 32 | 20 | 12 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k8-graph-tp2-eagerrecovery-promoteplus-20260618cu-000000-0-872a9442` | 1 | 9 | 8 | 0 | 0 | 9 | 9 |
| `cmpl-qwen36-oracle-k8-graph-tp2-eagerrecovery-promoteplus-20260618cu-000000-0-872a9442` | 2 | 9 | 8 | 0 | 0 | 9 | 9 |
| `cmpl-qwen36-oracle-k8-graph-tp2-eagerrecovery-promoteplus-20260618cu-000000-0-872a9442` | 3 | 9 | 3 | 5 | -6 | 3 | 3 |
| `cmpl-qwen36-oracle-k8-graph-tp2-eagerrecovery-promoteplus-20260618cu-000000-0-872a9442` | 4 | 9 | 1 | 7 | -8 | 1 | 1 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
