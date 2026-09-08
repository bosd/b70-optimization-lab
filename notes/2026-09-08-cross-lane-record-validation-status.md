# Which published records have actually been re-measured

The Flash-Next replay audit raised an obvious question for the rest of the repo: for any
published record, has anyone checked recently that it still reproduces? This is the status as
of 2026-09-08, with direct evidence where I have it and an honest "not checked" where I do not.

## Re-measured, and they reproduce

| lane | record | when re-measured | outcome |
| --- | --- | --- | --- |
| Flash-Next placement MTP1 | 31.929484 | 2026-09-08 (A335) | 32.1974, +0.84% |
| Flash-Next Triton-HC MTP1 | 37.045844 | 2026-09-08 (A331, A332) | 37.4261 / 37.1178 |
| Flash-Next fused-QSA MTP1 | 37.825654 | 2026-09-08 (A328, A329) | 37.6223 / 37.9462 |
| Flash-Next MTP0 W13-N32 | 33.797067 | 2026-09-08 (A334) | 33.8012, +0.004 |
| Flash-Next MTP0 W13-N64 | 34.495292 | 2026-09-08 (A325/A326/A333) | 34.4953–34.5201 |
| Gemma 4 26B A4B Q8, 1x B70 | 125 tok/s | 2026-09-07 (in-guide) | 115.3 host build, 111.2 / 116.3 container |

Every published value falls inside its own replay range on Flash-Next. The Gemma4 entry is
the guide's own clean-rebuild table, not something I ran; it reports 111–116 against a 125
record and calls those "same-recipe support runs, not new records", with the shortfall
attributed to the oneAPI 2026.1.1 compatibility build rather than to the recipe. **That gap
is larger than anything the Flash-Next audit found and is worth a closer look by whoever owns
that lane** — I have not investigated it and am not asserting the record is wrong.

## Re-measurement attempted and blocked

| lane | record | what happened |
| --- | --- | --- |
| MiniMax M2.7 INT4, 4x B70 | 110.896 total tok/s | 2026-09-08: the guide could not run. Two script defects fixed (silent `set -u` abort in the oneAPI source; `$VENV/lib` missing from the library path, leaving torch with 0 of 4 GPUs). The blocker that remains is structural: the venv's vLLM has been advanced to the qwen27-era tree for other lanes, so the record's 2026-05-23 runtime is not installed. Its evidence stands; its runtime does not. |

## Not re-measured

Everything else. Guides with no 2026-09 activity in their README include the MiniMax 89/94
tok/s lines, LFM2.5 26B, Ornith 15-35B, Nemotron 3.5 Lightning, Qwen3.6 27B AutoRound (both
guides), Qwen3.8 27B Q8 TP2, the Flash-Next MTP3 research snapshot, and the rapid-model
snapshots. That is not a criticism of them — most were correct when published — but nobody
has checked, and the MiniMax result shows what can rot underneath a guide that shares a venv.

## What the audit suggests as policy

1. **Records pinned by frozen packets survive; records pinned by a shared venv do not.** Every
   Flash-Next record replayed weeks on. The MiniMax guide could not run at all. The difference
   is not care taken at publication, it is whether the runtime is pinned by the packet.
2. **A single suite is not an error bar.** MTP1's suite-to-suite spread is 0.27–0.38 tok/s;
   MTP0's is 0.004–0.025. A derived claim of +0.78 between two MTP1 lineages became +0.60 once
   both sides had three suites.
3. **Re-measurement is cheap on idle cards.** The whole Flash-Next audit was about four hours
   overnight and corrected a published comparison, produced error bars for two promotions, and
   found 224 of 243 frozen clients no longer re-runnable.

## Evidence

- Flash-Next: `notes/2026-09-08-every-published-flash-next-record-replays.md` and the notes it cites.
- MiniMax: `notes/2026-09-08-minimax-m27-110tps-guide-revalidation.md`.
- Gemma4: the replay table in `repro/gemma4-26b-a4b-q8-b70-125tps-20260701/README.md`.
