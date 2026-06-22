# Qwen3.6 Spec Trace Replay

- trace: `/home/steve/llm-optimizations/data/qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-spec-trace.jsonl`
- rows: `14`
- malformed rows: `0`
- requests: `1`
- suppressed follow-up mismatches: `5`
- suppressed schedule mismatches: `8`
- suppressed accept mismatches: `8`
- accounting mismatches: `0`

| request | rows | drafts | accepted | rejected | suppressed rows | joined token case | generated mismatches | schedule mismatches | accept mismatches | accounting mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 14 | 14 | 9 | 5 | 9 | `natural_latency_plan (scheduler_prefix)` | 5 | 8 | 8 | 0 |

## Suppressed Follow-Up Mismatches

- request `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` line `1` -> `2`:
  suppressed `27044` ` dense`, next scheduled `47193` ` numbered`, next verifier token was `47193` ` numbered`, next emitted `47193` ` numbered`.
- request `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` line `2` -> `3`:
  suppressed `14246` ` engineering`, next scheduled `8129` ` notes`, next verifier token was `8129` ` notes`, next emitted `8129` ` notes`.
- request `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` line `3` -> `4`:
  suppressed `13` `.`, next scheduled `24985` ` Focus`, next verifier token was `24985` ` Focus`, next emitted `24985` ` Focus`.
- request `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` line `6` -> `7`:
  suppressed `1622` ` request`, next scheduled `4478` ` speed`, next verifier token was `16401` ` decode`, next emitted `None` `None`.
- request `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` line `12` -> `13`:
  suppressed `4131` ` quality`, next scheduled `13` `.`, next verifier token was `4557` ` loss`, next emitted `None` `None`.

## Request Counter Transitions

| request | line | scheduled | accepted | rejected | computed delta | output-token delta | token delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 1 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 2 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 3 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 4 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 5 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 6 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 7 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 8 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 9 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 10 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 11 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 12 | 2 | 1 | 0 | -1 | 1 | 1 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 13 | 2 | 0 | 1 | -2 | 0 | 0 |
| `cmpl-qwen36-oracle-k1-native-specprefillseq-currentbaseline-eager-tp2-20260617be-000000-0-94e68a7b` | 14 | 2 | 1 | 0 | -1 | 1 | 1 |

Post-output `computed_minus_tokens` is included in the JSON rows.
Values below zero usually mean the next pass may recompute an already
emitted token; values above zero after suppressing a bonus can mean stale
unemitted KV stayed live.
