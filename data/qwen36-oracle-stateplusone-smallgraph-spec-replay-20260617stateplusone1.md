# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-stateplusone-smallgraph-20260617a-spec.jsonl`
- rows: `29`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `14`
- suppressed schedule mismatches: `14`
- suppressed accept mismatches: `14`
- accounting mismatches: `2`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 19 | 19 | 18 | 1 | 18 | `repetitive_kernel_notes (scheduler_prefix)` | 11 | 11 | 11 | 1 |
| `cmpl-stateplusone20260617a-000000-0-b6e9f494` | 10 | 10 | 9 | 1 | 9 | `natural_latency_plan (scheduler_prefix)` | 3 | 3 | 3 | 1 |

## Suppressed Follow-Up Mismatches

- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `15` -> `16`:
  suppressed `2468` ` output`, next scheduled `1345` ` while`, next verifier token was `1345` ` while`, next emitted `1345` ` while`.
- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `16` -> `17`:
  suppressed `1345` ` while`, next scheduled `28043` ` measuring`, next verifier token was `28043` ` measuring`, next emitted `28043` ` measuring`.
- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `17` -> `18`:
  suppressed `28043` ` measuring`, next scheduled `7072` ` multi`, next verifier token was `7072` ` multi`, next emitted `7072` ` multi`.
- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `18` -> `19`:
  suppressed `7072` ` multi`, next scheduled `3817` ` token`, next verifier token was `3817` ` token`, next emitted `3817` ` token`.
- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `19` -> `20`:
  suppressed `3817` ` token`, next scheduled `22188` ` verification`, next verifier token was `22188` ` verification`, next emitted `22188` ` verification`.
- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `22` -> `23`:
  suppressed `15153` ` Intel`, next scheduled `1543` ` X`, next verifier token was `1543` ` X`, next emitted `1543` ` X`.
- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `24` -> `25`:
  suppressed `387` ` P`, next scheduled `16401` ` decode`, next verifier token was `16401` ` decode`, next emitted `16401` ` decode`.
- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `25` -> `26`:
  suppressed `16401` ` decode`, next scheduled `85683` ` verifier`, next verifier token was `85683` ` verifier`, next emitted `85683` ` verifier`.
- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `26` -> `27`:
  suppressed `85683` ` verifier`, next scheduled `15162` ` bucket`, next verifier token was `15162` ` bucket`, next emitted `15162` ` bucket`.
- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `27` -> `28`:
  suppressed `15162` ` bucket`, next scheduled `5832` ` route`, next verifier token was `5832` ` route`, next emitted `5832` ` route`.
- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `28` -> `29`:
  suppressed `5832` ` route`, next scheduled `271` `

`, next verifier token was `4618` ` graph`, next emitted `4618` ` graph`.
- request `cmpl-stateplusone20260617a-000000-0-b6e9f494` line `7` -> `8`:
  suppressed `24985` ` Focus`, next scheduled `383` ` on`, next verifier token was `383` ` on`, next emitted `383` ` on`.
- request `cmpl-stateplusone20260617a-000000-0-b6e9f494` line `8` -> `9`:
  suppressed `383` ` on`, next scheduled `3074` ` single`, next verifier token was `3074` ` single`, next emitted `3074` ` single`.
- request `cmpl-stateplusone20260617a-000000-0-b6e9f494` line `9` -> `10`:
  suppressed `3074` ` single`, next scheduled `43318` `-request`, next verifier token was `312` `--`, next emitted `312` `--`.

## Accounting Mismatches

- request `cmpl-stateplusone20260617a-000001-0-814b8dfe` line `29`: expected computed delta `-1` from rejected `1` plus suppressed `0`, observed `-2`.
- request `cmpl-stateplusone20260617a-000000-0-b6e9f494` line `10`: expected computed delta `-1` from rejected `1` plus suppressed `0`, observed `-2`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 11 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 12 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 13 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 14 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 15 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 16 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 17 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 18 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 19 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 20 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 21 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 22 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 23 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 24 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 25 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 26 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 27 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 28 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-stateplusone20260617a-000001-0-814b8dfe` | 29 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-stateplusone20260617a-000000-0-b6e9f494` | 1 | 2 | 1 | 0 | -1 | 1 | 1 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
