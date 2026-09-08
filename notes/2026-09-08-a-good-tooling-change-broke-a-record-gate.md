# A correct tooling change broke a record gate, and that is the pattern

Attempting to validate the Laguna S 2.1 125.462 tok/s record — the cheapest remaining target,
since its vLLM and kernel worktrees are both present — the gate stopped immediately:

```
Laguna formal M8 crossover leg: SHA256 drift: scripts/bench-openai-realistic-suite.py
```

## The change was right

Commit `80e76ccfb` (Codex agent, 2026-09-08 00:25) added hostname, kernel, CPU, RAM, GPU
count and device mask to all three benchmark harnesses. Its reason is a good one: the Gemma 4
replays that read as a 10% shortfall were a **cross-host** comparison, and establishing that
required counting GPU-index directory names across 824 record-era runs. The commit is careful
— the metadata never reaches the server or the timing path — and it prevents a class of wrong
conclusion. I had myself flagged that same Gemma4 gap as "unexplained" six hours after it was
explained; the correction is recorded in the validation-status note.

## And it broke a published record's gate

`repro/laguna-s-2.1-int4-b70-125tps-20260731/run-record-gate.sh` pins
`scripts/bench-openai-realistic-suite.py` by SHA256. The harness changed, so the pin no longer
matches and the Laguna record cannot be replayed without either reverting the script for the
run or re-pinning the gate.

This is the third instance of one structure in a single session:

| what pinned what | broke when | scope |
| --- | --- | --- |
| 243 frozen Flash-Next clients pin the W13-N32 verifier | verifier gained accepted heads | 224 of 243 no longer re-runnable |
| A301's client pins the exact-4K authority | lineage's authority moved | latent; found by A323 |
| Laguna's record gate pins `bench-openai-realistic-suite.py` | a correct metadata change today | record not replayable as written |

The common shape: **a frozen artifact pins shared, mutable tooling by hash.** Every
improvement to the shared tool invalidates every gate frozen before it. Nobody did anything
wrong in any of the three cases — the verifier had to gain heads, the harness had to record
its host — and the gates were right to pin.

## What I am not doing

I am not re-pinning the Laguna gate. Its hash is part of what the record attests, and updating
it silently would mean the gate no longer proves what it claimed to prove. That is the record
owner's call, and it is the same reason I left A272's stale verifier pin alone.

## What would fix the class

Version the shared tools rather than editing in place — `bench-openai-realistic-suite-<sha>.py`,
`verify-moe-m1-w13-n32-selection-<sha>.py` — so a pin always resolves and an improvement is a
new file rather than a break. It costs a symlink and a naming convention, and it is the
difference between "the record is reproducible" and "the record was reproducible on the day".

Filed for a deliberate decision; it touches 243 Flash-Next clients, the Laguna gate, and
whatever else pins these harnesses.

## Evidence

- Gate failure reproduced from `repro/laguna-s-2.1-int4-b70-125tps-20260731/run-record-gate.sh` (rc=2).
- `git show 80e76ccfb` — the change, its rationale, and its verification.
- Related: `notes/2026-09-08-frozen-clients-pin-a-moving-verifier.md`,
  `notes/2026-09-08-a323-a-third-confirmation-and-a-latent-pin-defect.md`.
