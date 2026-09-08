# Re-validating the MiniMax M2.7 110 tok/s guide: two bugs fixed, one structural blocker

Attempted a re-run of `repro/minimax-m27-b70-110tps-ubuntu24-20260523/` on the originating
host to confirm the record still reproduces. It does not, and the reasons are worth having.

## 1. The scripts died silently (fixed)

`scripts/04-verify-runtime.sh` exited 1 with **no output on either stream**. The cause:

```bash
set -euo pipefail
source /opt/intel/oneapi/compiler/2025.3/env/vars.sh >/dev/null 2>&1
```

Intel's `vars.sh` dereferences `SETVARS_CALL` (line 202) and then `OCL_ICD_FILENAMES`
(line 258), both unbound when it is sourced directly rather than through `setvars.sh`.
Under `set -u` that is fatal, and with both streams muted the abort is invisible — the
script simply stops. Verified against every installed version: 2025.3, 2026.0 and `latest`
all die under `set -u`; none die under `set -e` or `set -o pipefail` alone.

Fixed in the guide's four scripts by relaxing `-u` for the vendor script only and failing
loudly if it genuinely fails.

**This pattern is repo-wide.** About 95 scripts combine `set -u` with a muted oneAPI source,
across published repro guides, `scripts/` and `experiments/`. They are not all broken in the
same way — many are build scripts whose environment differs — but any of them run on a fresh
shell today will abort without saying why. I have not mass-edited them: several are frozen
packet material where an edit changes what a pin refers to. This note is the record; the fix
above is the pattern to apply when each is next touched.

## 2. Torch saw zero of four GPUs (fixed)

With the abort gone, `torch.xpu.device_count()` returned **0** on a machine whose four cards
`xpu-smi` reports at 45 W. Bisected to `configs/runtime-env.sh`:

```bash
export LD_LIBRARY_PATH="$VENV/lib/python3.12/site-packages/torch/lib:/opt/intel/oneapi/compiler/2025.3/lib:..."
```

`$VENV/lib` is missing. With only `torch/lib` ahead of the oneAPI 2025.3 libraries the loader
resolves a mismatched runtime and the devices disappear. Adding `$VENV/lib` first restores
`True 4` — and it is exactly the order the working Qwen lanes on this host use.

Neither `ZE_AFFINITY_MASK` nor `ONEAPI_DEVICE_SELECTOR` was implicated; each is fine alone and
together, and unsetting both still gave 0 until the library path was corrected.

## 3. The record's runtime is gone from this host (not fixed, and not fixable here)

The preflight now reaches its platform assertion and fails there:
`current_platform.device_type` is empty. The reason is structural. The venv's `vllm` is an
editable install pointing at `/home/steve/src/vllm`, and that tree has since been advanced
for other lanes to `44fc8fde09`, tag `qwen27-int4-exactness-stack-20260817` — vLLM
`0.20.2rc1.dev13+g9557d9108.d20260620`. The 2026-05-23 stack the record was measured on is no
longer installed.

So the honest status of that record today: **its evidence stands, and its runtime does not.**
Re-measuring it on this host means rebuilding the 2026-05-23 stack (the guide's
`03-build-stack.sh` exists for that) into a separate venv, not reusing the current one. That
is a multi-hour rebuild, not a validation run, and it should be a deliberate decision rather
than a side effect of a re-check.

The guide's `SRC_ROOT` default also pointed at `$FAST_AI_ROOT/src`, which no longer holds the
source trees; a fallback to `$HOME/src` is added so the historical path still wins where it
exists.

## What this does not say

It does not say the 110 tok/s record was wrong. Nothing here re-measures throughput. It says
the reproduction path had two real defects that would have blocked anyone on a current host,
and that the originating host has moved past the record's runtime.
