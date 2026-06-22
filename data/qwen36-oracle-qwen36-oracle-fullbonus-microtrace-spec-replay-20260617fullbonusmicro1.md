# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-fullbonus-microtrace-20260617a-spec.jsonl`
- rows: `15`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `0`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `0`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-fullbonusmicro20260617a-000000-0-b679d0f1` | 9 | 9 | 8 | 1 | 0 | `natural_latency_plan (scheduler_prefix)` | 0 | 0 | 0 | 0 |
| `cmpl-fullbonusmicro20260617a-000001-0-bc985615` | 6 | 6 | 6 | 0 | 0 | `repetitive_kernel_notes (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-fullbonusmicro20260617a-000000-0-b679d0f1` | 1 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000000-0-b679d0f1` | 2 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000000-0-b679d0f1` | 3 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000000-0-b679d0f1` | 4 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000000-0-b679d0f1` | 5 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000000-0-b679d0f1` | 6 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000000-0-b679d0f1` | 7 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000000-0-b679d0f1` | 8 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000000-0-b679d0f1` | 9 | 2 | 0 | 1 | -1 | 1 | 1 |
| `cmpl-fullbonusmicro20260617a-000001-0-bc985615` | 10 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000001-0-bc985615` | 11 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000001-0-bc985615` | 12 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000001-0-bc985615` | 13 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000001-0-bc985615` | 14 | 2 | 1 | 0 | 0 | 2 | 2 |
| `cmpl-fullbonusmicro20260617a-000001-0-bc985615` | 15 | 2 | 1 | 0 | 0 | 2 | 2 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
