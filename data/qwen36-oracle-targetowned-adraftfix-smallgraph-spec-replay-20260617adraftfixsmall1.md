# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-targetowned-adraftfix-smallgraph-20260617a-spec.jsonl`
- rows: `4`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `2`
- suppressed schedule mismatches: `0`
- suppressed accept mismatches: `2`
- accounting mismatches: `2`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-targetadraftsmall20260617a-000000-0-b7ac57d7` | 2 | 2 | 1 | 1 | 1 | `natural_latency_plan (scheduler_prefix)` | 1 | 0 | 1 | 1 |
| `cmpl-targetadraftsmall20260617a-000001-0-8584ed2d` | 2 | 2 | 1 | 1 | 1 | `repetitive_kernel_notes (scheduler_prefix)` | 1 | 0 | 1 | 1 |

## Suppressed Follow-Up Mismatches

- request `cmpl-targetadraftsmall20260617a-000000-0-b7ac57d7` line `1` -> `2`:
  suppressed `27044` ` dense`, next scheduled `27044` ` dense`, next verifier token was `139349` `却没`, next emitted `139349` `却没`.
- request `cmpl-targetadraftsmall20260617a-000001-0-8584ed2d` line `3` -> `4`:
  suppressed `13` `.`, next scheduled `13` `.`, next verifier token was `123546` `皆可`, next emitted `123546` `皆可`.

## Accounting Mismatches

- request `cmpl-targetadraftsmall20260617a-000000-0-b7ac57d7` line `2`: expected computed delta `-1` from rejected `1` plus suppressed `0`, observed `-2`.
- request `cmpl-targetadraftsmall20260617a-000001-0-8584ed2d` line `4`: expected computed delta `-1` from rejected `1` plus suppressed `0`, observed `-2`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-targetadraftsmall20260617a-000000-0-b7ac57d7` | 1 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetadraftsmall20260617a-000000-0-b7ac57d7` | 2 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-targetadraftsmall20260617a-000001-0-8584ed2d` | 3 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-targetadraftsmall20260617a-000001-0-8584ed2d` | 4 | 2 | 0 | 1 | -2 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
