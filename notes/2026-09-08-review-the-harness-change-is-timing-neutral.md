# Review: the harness metadata change is timing-neutral, so re-pinning is safe

The Laguna record gate is blocked by SHA256 drift on
`scripts/bench-openai-realistic-suite.py`, caused by commit `80e76ccfb`, which added
host metadata to three benchmark harnesses. Whether to re-pin the gate is the record owner's
call, but the question underneath it is answerable now: **can that change have affected a
measurement?** If not, re-pinning is bookkeeping. If so, it is a much larger problem.

Reviewed, and it cannot.

## Where the call sits

`_measuring_host()` is invoked exactly once per harness, inside the final `result = {...}`
assembly, next to `created_at_utc`:

| harness | call line | file lines | timing or request calls after it |
| --- | --- | --- | --- |
| `bench-openai-realistic-suite.py` | 835 | 870 | **0** |
| `bench-openai-concurrency-oracle.py` | 438 | 505 | **0** |
| `bench-openai-long-context-suite.py` | 451 | 480 | **0** |

No `perf_counter`, `time.monotonic`, `urlopen` or request call appears after the metadata is
gathered in any of the three. The measurement is complete before the helper runs.

## What the helper does

Reads `/proc/cpuinfo` and `/proc/meminfo`, calls `platform.node()`/`release()`, runs
`xpu-smi discovery` once with a 20-second timeout, and copies `ZE_AFFINITY_MASK` and
`ONEAPI_DEVICE_SELECTOR` if set. Every filesystem and subprocess access is wrapped in
`try/except` returning partial data, so a missing `xpu-smi` degrades the metadata instead of
failing the run. Nothing is sent to the server; nothing is read back into the timing path.

The one thing worth naming: it does spawn a subprocess. Spawning `xpu-smi` *during* a
measurement could perturb it. It does not — it runs after — but that is a property of where
the call sits, not of the helper, so the placement is load-bearing and should stay where it is.

## Conclusion

The commit's own claim — "none of these values reach the server or the timing path" — holds
under review on all three harnesses. A result produced by the new harness is comparable with
one produced by the old.

**Therefore re-pinning the Laguna gate to the new hash would not weaken what the gate
attests about performance.** It remains the record owner's decision, because a gate's pin is
part of what a record claims and changing it is not mine to do silently; but the decision can
be made on bookkeeping grounds rather than on measurement risk.

The broader fix — versioning shared tools so pins always resolve — is still the thing that
stops this recurring, and is filed separately.

## Evidence

- `git show 80e76ccfb` and the three harnesses at their current revisions.
- Call-site line numbers and the post-call scan for timing and request calls, above.
- Related: `notes/2026-09-08-a-good-tooling-change-broke-a-record-gate.md`.
