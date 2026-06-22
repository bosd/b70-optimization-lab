# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k2-resume-20260617a-spec.jsonl`
- rows: `17`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `1`
- suppressed schedule mismatches: `1`
- suppressed accept mismatches: `1`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 11 | 22 | 18 | 4 | 1 | `natural_latency_plan (scheduler_prefix)` | 1 | 1 | 1 | 0 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000001-0-be0df4bb` | 6 | 12 | 9 | 3 | 0 | `repetitive_kernel_notes (scheduler_prefix)` | 0 | 0 | 0 | 0 |

## Suppressed Follow-Up Mismatches

- request `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` line `9` -> `10`:
  suppressed `198` `
`, next scheduled `13` `.`, next verifier token was `13` `.`, next emitted `None` `None`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 1 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 2 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 3 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 4 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 5 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 6 | 3 | 1 | 1 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 7 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 8 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 9 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 10 | 3 | 1 | 1 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000000-0-995c5b9e` | 11 | 3 | 0 | 2 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000001-0-be0df4bb` | 12 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000001-0-be0df4bb` | 13 | 3 | 1 | 1 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000001-0-be0df4bb` | 14 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000001-0-be0df4bb` | 15 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000001-0-be0df4bb` | 16 | 3 | 2 | 0 | 0 | 3 | 3 |
| `cmpl-qwen36-oracle-k2-resume128-20260617a-000001-0-be0df4bb` | 17 | 3 | 0 | 2 | -3 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
