# A record gate has been broken for two weeks, and today's change is not why

> **Corrected 2026-09-08 07:50, after this note was first written.** The title and framing
> below originally blamed commit `80e76ccfb` (today, 00:25) for breaking the Laguna gate.
> That is wrong. The gate pins `bench-openai-realistic-suite.py` at `40a483d9…`, which is
> revision `05741b1db` of **2026-07-19**. Four commits have touched that file since, and the
> **first drift was `b8858afac` on 2026-08-25** — two weeks ago. Today's commit is merely the
> most recent of four, and would have found the gate already broken. I checked the current
> hash against the pin, saw the newest commit in `git log`, and drew a causal line that the
> history does not support. The structural point below stands and is if anything stronger:
> the gate has been silently unrunnable for two weeks and nobody noticed, because nobody
> tried to replay the record.


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
| Laguna's record gate pins `bench-openai-realistic-suite.py` | first drift 2026-08-25 (`b8858afac`); three more since | record not replayable as written, and silently so for two weeks |

The common shape: **a frozen artifact pins shared, mutable tooling by hash.** Every
improvement to the shared tool invalidates every gate frozen before it. Nobody did anything
wrong in any of the three cases — the verifier had to gain heads, the harness had to record
its host — and the gates were right to pin.


## How long it was broken, and why that matters more than what broke it

| revision | date | matches the gate's pin? |
| --- | --- | --- |
| `05741b1db` | 2026-07-19 | yes — this is what the gate pins |
| `b8858afac` | 2026-08-25 | no — **first drift** |
| `2a303ad7b` | 2026-08-27 | no |
| `055e81178` | 2026-08-27 | no |
| `80e76ccfb` | 2026-09-08 | no |

The gate has been unrunnable since 2026-08-25 and nothing surfaced it, because in those two
weeks nobody tried to replay the Laguna record. A pin only fails when someone exercises it,
so a gate that is never run is indistinguishable from a gate that passes. That is the real
lesson: the Flash-Next audit found 224 clients in the same state, and the only reason it
found them is that something finally ran them.

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
