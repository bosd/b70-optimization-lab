# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k2-resume-nobonus-20260617a-spec.jsonl`
- rows: `28`
- malformed rows: `0`
- requests: `2`
- suppressed follow-up mismatches: `25`
- suppressed schedule mismatches: `25`
- suppressed accept mismatches: `25`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 14 | 28 | 26 | 2 | 13 | `natural_latency_plan (scheduler_prefix)` | 13 | 13 | 13 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` | 14 | 28 | 25 | 3 | 12 | `repetitive_kernel_notes (scheduler_prefix)` | 12 | 12 | 12 | 0 |

## Suppressed Follow-Up Mismatches

- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `1` -> `2`:
  suppressed `47193` ` numbered`, next scheduled `27044` ` dense`, next verifier token was `27044` ` dense`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `2` -> `3`:
  suppressed `14246` ` engineering`, next scheduled `47193` ` numbered`, next verifier token was `47193` ` numbered`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `3` -> `4`:
  suppressed `8129` ` notes`, next scheduled `14246` ` engineering`, next verifier token was `14246` ` engineering`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `4` -> `5`:
  suppressed `13` `.`, next scheduled `8129` ` notes`, next verifier token was `8129` ` notes`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `5` -> `6`:
  suppressed `24985` ` Focus`, next scheduled `13` `.`, next verifier token was `13` `.`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `6` -> `7`:
  suppressed `383` ` on`, next scheduled `24985` ` Focus`, next verifier token was `24985` ` Focus`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `7` -> `8`:
  suppressed `3074` ` single`, next scheduled `383` ` on`, next verifier token was `383` ` on`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `8` -> `9`:
  suppressed `43318` `-request`, next scheduled `3074` ` single`, next verifier token was `3074` ` single`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `9` -> `10`:
  suppressed `16401` ` decode`, next scheduled `43318` `-request`, next verifier token was `43318` `-request`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `10` -> `11`:
  suppressed `4478` ` speed`, next scheduled `16401` ` decode`, next verifier token was `16401` ` decode`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `11` -> `12`:
  suppressed `11` `,`, next scheduled `4478` ` speed`, next verifier token was `4478` ` speed`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `12` -> `13`:
  suppressed `29541` ` reliability`, next scheduled `11` `,`, next verifier token was `11` `,`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` line `13` -> `14`:
  suppressed `33389` ` gates`, next scheduled `29541` ` reliability`, next verifier token was `4779` ` memory`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `15` -> `16`:
  suppressed `78503` ` Preserve`, next scheduled `13` `.`, next verifier token was `13` `.`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `16` -> `17`:
  suppressed `4581` ` exact`, next scheduled `78503` ` Preserve`, next verifier token was `78503` ` Preserve`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `17` -> `18`:
  suppressed `2468` ` output`, next scheduled `4581` ` exact`, next verifier token was `4581` ` exact`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `18` -> `19`:
  suppressed `1345` ` while`, next scheduled `2468` ` output`, next verifier token was `2468` ` output`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `19` -> `20`:
  suppressed `28043` ` measuring`, next scheduled `1345` ` while`, next verifier token was `1345` ` while`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `20` -> `21`:
  suppressed `7072` ` multi`, next scheduled `28043` ` measuring`, next verifier token was `28043` ` measuring`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `21` -> `22`:
  suppressed `3817` ` token`, next scheduled `7072` ` multi`, next verifier token was `7072` ` multi`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `22` -> `23`:
  suppressed `22188` ` verification`, next scheduled `3817` ` token`, next verifier token was `3817` ` token`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `23` -> `24`:
  suppressed `13` `.`, next scheduled `22188` ` verification`, next verifier token was `22188` ` verification`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `24` -> `25`:
  suppressed `15153` ` Intel`, next scheduled `13` `.`, next verifier token was `13` `.`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `25` -> `26`:
  suppressed `1543` ` X`, next scheduled `15153` ` Intel`, next verifier token was `15153` ` Intel`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` line `26` -> `27`:
  suppressed `6126` `PU`, next scheduled `1543` ` X`, next verifier token was `1543` ` X`, next emitted `None` `None`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 1 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 2 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 3 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 4 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 5 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 6 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 7 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 8 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 9 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 10 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 11 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 12 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 13 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000000-0-a0d79342` | 14 | 3 | 0 | 2 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` | 15 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` | 16 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` | 17 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` | 18 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` | 19 | 3 | 2 | 0 | -3 | 0 | 0 |
| `cmpl-qwen36-oracle-k2-resume-nobonus128-20260617a-000001-0-b970a93c` | 20 | 3 | 2 | 0 | -3 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
