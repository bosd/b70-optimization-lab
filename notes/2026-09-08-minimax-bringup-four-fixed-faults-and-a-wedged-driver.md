# MiniMax M2.7 bring-up: four fixed faults, one real regression, and a wedged driver

Picking the MiniMax INT4 record back up on today's host. The serve failed at engine init;
this is the chain, each step confirmed before moving on, and the point where it stopped.

## 1. Loader path (fixed earlier)

`VLLM_XPU_*` platform resolution failed with `libgdn_attn_kernels_xe_2.so: cannot open
shared object file`, so vLLM silently resolved `UnspecifiedPlatform`. `configs/runtime-env.sh`
is sourced *before* the venv is activated, so asking `python3` on PATH for the kernels
directory returned empty; asking `$VENV/bin/python` fixes it.

## 2. The four-worker SIGSEGV at distributed init

All four workers took SIGSEGV at address `(nil)` immediately after oneCCL's
topology-recognition warning, before the model was loaded. The named frames:

    arc_ll256_allreduce  <-  arc_allreduce  <-  allreduce_sycl_single_node

A minimal four-rank harness reproduces this without vLLM at all: a **1-element (4 byte)
float32 allreduce crashes**, while 256 B and larger are fine. vLLM's distributed-init
sanity collective is exactly that shape.

`CCL_ENABLE_SYCL_KERNELS=0` passes all 25 size/dtype cases and fixes the server. Narrower
knobs do **not** help, each tried and each still crashing on the first 4-byte allreduce:

| knob | result |
| --- | --- |
| `CCL_SYCL_ALLREDUCE_ARC=0` | still crashes |
| `CCL_SYCL_ALLREDUCE_LL_THRESHOLD=0` | still crashes |
| `CCL_SYCL_ALLREDUCE_SMALL_THRESHOLD=0` | still crashes |
| `CCL_SYCL_ALLREDUCE_TMP_BUF=1` | still crashes |
| `CCL_ATL_TRANSPORT=mpi` | still crashes |
| `CCL_ENABLE_SYCL_KERNELS=0` | **25/25 pass** |

Worth recording separately: `CCL_SYCL_ALLREDUCE_SIMPLE_THRESHOLD` and its ALLGATHERV and
REDUCE_SCATTER siblings, which the working Qwen lanes set, are **not knobs this libccl
knows** -- they do not appear in the library's own environment-variable table and oneCCL
never reports them as changed. They are inert wherever they are set on this host.

Three other differences from the working lanes were brought over on the way (device
selector unset, `FI_PROVIDER=tcp`/`FI_TCP_IFACE=lo`, `CCL_ZE_IPC_EXCHANGE=pidfd`,
`VLLM_WORKER_MULTIPROC_METHOD=spawn`). None of them fixed the segfault -- each was tested
and each still produced four dead workers. They are kept because they match the lanes that
work, but they are not the fix and should not be described as one.

## 3. `MoERunner` missing `shared_expert_gate`

With the workers alive, `~/src/vllm` raised
`TypeError: MoERunner.__init__() got an unexpected keyword argument 'shared_expert_gate'`.
`FusedMoE.__init__` (layer.py:437) always forwards the gate; that tree's runner never
accepted it, and nothing in its runner package reads it. Fixed in `~/src/vllm` by accepting
the parameter and raising `NotImplementedError` for a non-`None` gate rather than silently
dropping it. MiniMax M2.7 has `shared_intermediate_size: 0`, so its gate is `None` and
ignoring it is correct for this model. The sibling tree `~/src/vllm-current-main` already
carries the full FSE implementation; this tree is simply at a broken intermediate state.

## 4. The actual regression: the INT4 MoE path is not in `~/src/vllm`

Next failure was `torch.OutOfMemoryError` -- with the giveaway frame
`unquantized_fused_moe_method.py`. vLLM resolved `quantization=inc` but logged
`Using XPU Unquantized MoE backend`, so the INT4 weights were being inflated.

`INCConfig.apply_xpu_w4a16_quant_layer` returns `None` for anything that is not
`LinearBase`/`ParallelLMHead` -- including `FusedMoE` -- so INC on XPU supplies no MoE
method. That is true at HEAD *and* at the tree state of the record date, so inc.py was
never the source of the INT4 MoE path.

The record does not run stock vLLM. `scripts/03-build-stack.sh` checks out
`c51df4300` and applies a 41-file patch carried by the earlier 89 tok/s guide,
`repro/minimax-m27-b70-89tps-20260520/patches/vllm-active-promoted-minimax-89tps-20260520.patch.gz.b64`.
That patch is what supplies the INT4 MoE path: `moe_wna16.py` reading
`VLLM_XPU_USE_LLM_SCALER_MOE`, plus a tuned `int4_w4a16` MoE config for this device
(`E=256,N=384,device_name=Intel(R)_Graphics_[0xe223]`). `$SRC_ROOT/vllm` has moved on to
unrelated work and carries none of it -- the knob is read nowhere in that tree, which is
why vLLM reported `Unknown vLLM environment variable detected: VLLM_XPU_USE_LLM_SCALER_MOE`.

Reproduction detail worth keeping: the README's "vLLM source commit `c51df4300`" is the
*base*, not the served tree. The served tree is that commit **plus** the patch. Anyone
reading the pin alone gets an unquantized model that cannot fit.

Set up as a detached worktree at `~/src/vllm-minimax-record` (patch applies cleanly, 41
files), with `configs/runtime-env.sh` preferring it. `~/src/vllm` main is left alone.

Also confirmed on the way: five of the six llm-scaler ESIMD modules no longer import
against the current torch (`undefined symbol: torch::Library::_def(...)`, a C++ ABI break);
only `moe_int4_ops`, rebuilt 2026-06-03, still loads. The record's build script only ever
builds `setup_moe_int4_only.py`, so this is not necessarily fatal, but the other five are
dead weight until rebuilt.

## 5. Where it stopped: the `xe` driver wedged

The run against the patched worktree produced **zero** log lines while burning ~985 s of
system time against 3.7 s of user time, with the DRM render nodes open and no workers
spawned. dmesg explains it:

    watchdog: BUG: soft lockup - CPU#7 stuck for 153s! [xpu-smi:1057446]
    ... xe_query_ioctl+0x78/0x150 [xe]  <-  xe_drm_ioctl+0x61/0xb0 [xe]

45 soft lockups. The vLLM process and two `xpu-smi` processes are all stuck in
`xe_query_ioctl` and survive SIGKILL; two earlier workers are unreapable zombies.

**Probable trigger, and a lesson:** I was polling `xpu-smi stats -d 0` every 25 s to watch
memory while the engine was initialising. Concurrent `xe_query_ioctl` from xpu-smi during
device init is the common factor, and xpu-smi is the task the watchdog names. Do not poll
xpu-smi against cards that a server is currently bringing up -- read the server's own log
instead. This is the same class as the torch-profiler and expandable_segments findings: the
measurement perturbed the thing measured, only here it took the driver down with it.

Recovering the cards needs privileged action and the user's go-ahead; nothing further can
be measured until then. The four fixes above are independent of that and stand on their own.
