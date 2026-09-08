# Resume here: MiniMax bring-up, after the 2026-09-08 reboot

The reboot was to clear an `xe` driver wedge (soft lockups in `xe_query_ioctl`, processes
surviving SIGKILL, module refcount 93). Full diagnosis:
`notes/2026-09-08-minimax-bringup-four-fixed-faults-and-a-wedged-driver.md`.

## Post-reboot routine first

1. Remount the model store: `/dev/sda2` via ntfs-3g to `/mnt/usb-models`.
2. `xe` reload only if the cards do not enumerate.
3. Tune.
4. Confirm all four cards enumerate before launching anything.

## Then: the MiniMax run that never got a number

Everything below is already committed and in place -- no re-diagnosis needed.

    cd repro/minimax-m27-b70-110tps-ubuntu24-20260523
    bash scripts/06-serve-openai-compatible.sh > /tmp/q38-attempt-logs/minimax-serve-9.log 2>&1

`configs/runtime-env.sh` already carries all four fixes and already prefers the patched
worktree `~/src/vllm-minimax-record` (detached at `c51df4300` + the 41-file
`vllm-active-promoted-minimax-89tps` patch, which is what supplies the INT4 MoE path).

Expected: workers survive init (no `arc_ll256_allreduce` segfault), `quantization=inc`,
and the MoE backend line must **not** say `Unquantized` -- if it does, the worktree is not
being picked up and the model will OOM rather than fit.

**Do not poll `xpu-smi` while the engine is initialising.** That is what wedged the driver.
Watch the log. A load emitting zero log lines with high system time is the driver bug, not
a slow load -- check `/proc/<pid>/stat` utime vs stime.

Once it serves, take the throughput number and compare against the 110 tok/s record before
claiming anything about it.

## Known-open, not blocking

- Five of six llm-scaler ESIMD modules fail to import against current torch
  (`undefined symbol: torch::Library::_def`). Only `moe_int4_ops` loads, and the record's
  build script only ever builds that one -- so this may not matter, but they are dead
  weight until rebuilt.
- The record README's "vLLM source commit c51df4300" is the base, not the served tree.
  Worth correcting in the guide so the next reader does not get an unquantized model.
