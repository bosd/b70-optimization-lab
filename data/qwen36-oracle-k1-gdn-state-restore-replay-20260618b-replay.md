# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-gdn-state-restore-replay-20260618b-spec-trace.jsonl`
- rows: `13`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `11`
- suppressed schedule mismatches: `11`
- suppressed accept mismatches: `11`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 13 | 13 | 11 | 2 | 11 | `natural_latency_plan (scheduler_prefix)` | 11 | 11 | 11 | 0 |

## Suppressed Follow-Up Mismatches

- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `1` -> `2`:
  suppressed `27044` ` dense`, next scheduled `47193` ` numbered`, next verifier token was `47193` ` numbered`, next emitted `47193` ` numbered`.
- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `2` -> `3`:
  suppressed `14246` ` engineering`, next scheduled `8129` ` notes`, next verifier token was `8129` ` notes`, next emitted `8129` ` notes`.
- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `3` -> `4`:
  suppressed `13` `.`, next scheduled `24985` ` Focus`, next verifier token was `24985` ` Focus`, next emitted `24985` ` Focus`.
- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `4` -> `5`:
  suppressed `383` ` on`, next scheduled `3074` ` single`, next verifier token was `3074` ` single`, next emitted `3074` ` single`.
- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `5` -> `6`:
  suppressed `43318` `-request`, next scheduled `16401` ` decode`, next verifier token was `16401` ` decode`, next emitted `16401` ` decode`.
- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `6` -> `7`:
  suppressed `4478` ` speed`, next scheduled `11` `,`, next verifier token was `11` `,`, next emitted `11` `,`.
- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `7` -> `8`:
  suppressed `29541` ` reliability`, next scheduled `33389` ` gates`, next verifier token was `33389` ` gates`, next emitted `33389` ` gates`.
- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `8` -> `9`:
  suppressed `11` `,`, next scheduled `321` ` and`, next verifier token was `4779` ` memory`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `10` -> `11`:
  suppressed `4131` ` quality`, next scheduled `4557` ` loss`, next verifier token was `4557` ` loss`, next emitted `4557` ` loss`.
- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `11` -> `12`:
  suppressed `13` `.`, next scheduled `271` `

`, next verifier token was `271` `

`, next emitted `271` `

`.
- request `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` line `12` -> `13`:
  suppressed `248068` `<think>`, next scheduled `271` `

`, next verifier token was `198` `
`, next emitted `None` `None`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 1 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 2 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 3 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 4 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 5 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 6 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 7 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 8 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 9 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 10 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 11 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 12 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-gdn-state-restore-replay-20260618b-000000-0-a6ca038e` | 13 | 2 | 0 | 1 | -2 | 0 | 0 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
