# Which repro guides can actually be run today

Two attempts to validate a record this session were blocked not by the recipe but by a
dependency that is no longer on the host — MiniMax's vLLM runtime, then Muse-Glimmer's
llama.cpp tree. Discovering that one guide at a time is expensive, so this is the inventory.

## Models

Ten guides name a model path. **Nine resolve.** The exception was
`qwen38-27b-autoround-int4-b70`, whose runnable block pointed at a `gptq-relabel` directory
that no longer exists; annotated with the live path (fixed in `ce230a4d6`). Model storage is
in good shape.

## Runtimes

Fifteen guides name a runtime tree under `~/src` or `/mnt/fast-ai/runtime`. **Three name at
least one that is absent:**

| guide | absent runtime | rebuildable from the guide? |
| --- | --- | --- |
| `deepseek-v4-flash-k160-b70-80tps-20260718` | `deepseek-v4-vllm-record-264c7f2f7-exact`, `deepseek-v4-xpu-kernels-record-313156737-exact` | guide ships `scripts/build-clean-runtime.sh` |
| `muse-glimmer-30b-q8-woq-b70-100tps-20260813` | `llama.cpp-muse-q8-woq-repro` | yes — `restore-source.sh` + `build.sh` |
| `qwen38-27b-autoround-int4-b70` | `oneccl-public-qwen27`, `oneccl-public-qwen27-build` | oneCCL build documented in `ONECCL-BUILD-20260818.md` |

All three ship their own restore-and-build path, so none is lost — but none is a
*quick* validation either. Replaying any of them means a source build first, which is a
deliberate job rather than something to start on idle cards without saying so.

## What is cheap to validate right now

The Flash-Next guides (all four) and the Gemma4 and Laguna guides have their runtimes
present. Flash-Next is fully re-measured as of today. **Gemma4 and Laguna are the cheapest
unvalidated targets**, and Gemma4 already carries in-guide replays from 2026-09-07 showing
111–116 against a 125 record, which is the largest unexplained gap currently visible in the
repo and belongs to that lane's owner.

## The pattern worth naming

MiniMax's runtime is gone because its venv is shared and was advanced for other lanes.
Muse-Glimmer's and DeepSeek's are gone because a source tree under `~/src` was not preserved.
Flash-Next's survive because its packets pin a stage directory and an overlay commit, and
both are still on disk. The lesson from the record audit — that frozen packets survive and
shared or unpinned environments do not — shows up again here, one layer down: it applies to
the *runtime trees* as much as to the records.

## Evidence

- Model inventory: every `/mnt/*/llm-models/*` path named in a `repro/*/README.md`.
- Runtime inventory: every `~/src/*` and `/mnt/fast-ai/runtime/*` path named in any
  `repro/*/**.sh` or `**.md`, checked for existence.
- Related: `notes/2026-09-08-cross-lane-record-validation-status.md`,
  `notes/2026-09-08-minimax-m27-110tps-guide-revalidation.md`.
