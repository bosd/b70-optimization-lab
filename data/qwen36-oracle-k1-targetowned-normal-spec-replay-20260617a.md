# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-targetowned-normal-20260617a-spec.jsonl`
- rows: `22`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `2`
- suppressed schedule mismatches: `1`
- suppressed accept mismatches: `2`
- accounting mismatches: `2`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 17 | 17 | 16 | 1 | 16 | `natural_latency_plan (scheduler_prefix)` | 1 | 1 | 1 | 1 |
| `cmpl-targetowned20260617a-000001-0-ad63ab68` | 5 | 5 | 4 | 1 | 4 | `repetitive_kernel_notes (scheduler_prefix)` | 1 | 0 | 1 | 1 |

## Suppressed Follow-Up Mismatches

- request `cmpl-targetowned20260617a-000000-0-95d9632a` line `16` -> `17`:
  suppressed `15153` ` Intel`, next scheduled `11436` ` hardware`, next verifier token was `19087` ` Arc`, next emitted `19087` ` Arc`.
- request `cmpl-targetowned20260617a-000001-0-ad63ab68` line `21` -> `22`:
  suppressed `2468` ` output`, next scheduled `2468` ` output`, next verifier token was `271` `

`, next emitted `271` `

`.

## Accounting Mismatches

- request `cmpl-targetowned20260617a-000000-0-95d9632a` line `17`: expected computed delta `-1` from rejected `1` plus suppressed `0`, observed `-2`.
- request `cmpl-targetowned20260617a-000001-0-ad63ab68` line `22`: expected computed delta `-1` from rejected `1` plus suppressed `0`, observed `-2`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 1 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 2 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 3 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 4 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 5 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 6 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 7 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 8 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 9 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 10 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 11 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 12 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 13 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 14 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 15 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 16 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000000-0-95d9632a` | 17 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-targetowned20260617a-000001-0-ad63ab68` | 18 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000001-0-ad63ab68` | 19 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetowned20260617a-000001-0-ad63ab68` | 20 | 2 | 1 | 0 | -1 | 1 | 1 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
