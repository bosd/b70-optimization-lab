# Reproduce the Qwen3.8 Flash-Next lossless-MTP1 line with both of the model's reference Triton kernels on XPU (37.825654 tok/s on four B70s)

> **Certification: `lab-replay`.** This replays the record on a host where the
> lab's vLLM overlay, kernel stage, oneCCL build, model copy, virtual
> environment, and four-card topology already exist. Every identity is pinned
> and every binary is hosted, but the guide is not a portable installer; its
> `missing` entry in [`repro/guide-catalog.json`](../guide-catalog.json) lists
> the open gates. The [container route](CONTAINER-STATUS.md) is written but
> unbuilt and unreplayed (the base image ships torch 2.13; the record needs 2.11).

This is the fastest Flash-Next line the lab has published. It completes a pair of
**reference restorations**: the XPU port of this model had replaced two of the model's
own Triton kernels, and this line runs both. The hyper-connection glue (gate-mix,
combine, combine-norm, silu) ran on torch fallbacks, restored in the
[37.05 tok/s line](../qwen38-flash-next-fp8-tp4-mtp1-hctriton-b70-37tps-20260907/README.md);
the QSA pre-indexer ran as an unfused sequence of qk projection, query norm and rope,
group compression, compressed-key norm and rope and two or three cache-row stores,
which a per-phase timing split put at 18.0 of the indexer's 23.9 ms per eager step.
Both sit on the deterministic full-decode-graph TP4/EP4 server with one publisher MTP
token and never-routed experts host-placed (the
[31.93 tok/s placement line](../qwen38-flash-next-fp8-tp4-mtp1-placement-b70-32tps-20260906/README.md)).
The MoE kernel, its tuned map, the offload and the placement are untouched.

The outputs are a **new authority and the difference is at depth, not in quality**.
Exact-2K coincides with the certified stream (`afffd211…`); exact-4K does not
(`1d833e5f…` rather than `c6193cc6…`), so a consumer who pinned 4K outputs must re-pin.
What the line preserves is the quality profile, byte for byte against the certified
battery: seven of seven exact-case outputs identical, sixteen repeats collapsing to one
hash, the long-context needle identical. Every pin is deterministic across servers, and
within the lineage MTP1 remains lossless, reproducing the MTP0 pins at both depths.
LocalMaxxing approved it as run
[`cmtrmp3mj001fps01thcathd0`](https://www.localmaxxing.com/runs/cmtrmp3mj001fps01thcathd0); the MTP0 twin is run
[`cmtrmp37v001bps01a7fi46nf`](https://www.localmaxxing.com/runs/cmtrmp37v001bps01a7fi46nf)
(33.797067 tok/s).

## Result and identity

| Item | Value |
| --- | --- |
| Headline | **37.825654 tok/s**, median of prompt-class medians over 99 inter-token intervals after TTFT, fixed cold 12-prompt realistic suite sent once (A306, 2026-09-07); the placement line scored 31.929484 on the same suite |
| Exactness | New authority, and the change is at depth: exact-2K **coincides** with the certified stream (`afffd211…`) while exact-4K does not (`1d833e5f…` in place of `c6193cc6…`). Both pins reproduced across the A297, A299, A300 and A304 MTP0 servers and the A305 MTP1 server; within the lineage MTP1 is lossless, reproducing the MTP0 pins at both depths; twelve suite rows fresh (cached_tokens 0) and deterministic |
| Quality | 6/7 exact cases with the inherited `code_execution` miss and byte-identical outputs to the certified placement battery on all seven, 16/16 repeats one hash, 2,157-token needle found (A304 and A305 batteries) |
| Model | `Qwen/Qwen3.8-Flash-Next-FP8` revision `bcd9f01ddc9cff2316eb84281bebcd5b058bddce` (131 shards, 185,563,783,127 bytes; [contract](../qwen38-flash-next-fp8-tp4-mtp3-b70/model-contract.json)) |
| vLLM | fused-QSA overlay `6d8724577dabbee5fa0bbc70c4d927c6174c8d8a` (tree `3e8dfc59…`): two commits over the Triton-HC MTP1 head `62219122`, itself one commit over the placement head `005dc578` ([series](../../patches/qwen38-flash-next-fp8-b70/vllm-qsafused-mtp1-6d872457/README.md)); the MTP0 twin is `2a372e86` on `cb59004b` |
| XPU kernel stage | build head `2f829747503c77d4814834dffd0840fb1dd9f75a`, 18 loadable files pinned by [`runtime-stage.sha256`](../qwen38-flash-next-fp8-tp4-mtp3-b70/runtime-stage.sha256) |
| Collective runtime | public oneCCL `4ceafd1` build, `libccl.so.1.0` `43d94d43…`, `kernels.spv` `0d549c35…` ([receipt](../../patches/qwen38-flash-next-fp8-b70/oneccl-4ceafd1-b70-public/README.md)) |
| Python runtime | Python 3.12 venv, `torch 2.11.0+xpu`, `triton 3.7.0`, oneAPI 2025.3 compiler runtime |
| Cards | four Intel Arc Pro B70 32 GiB, TP4 + EP4, `ZE_AFFINITY_MASK=0,1,2,3` |
| Configuration | as the placement line (`FULL_DECODE_ONLY` graph, MTP `num_speculative_tokens=1`, max length 4,352, one sequence, 64 batched tokens, KV `376569856` bytes BLHNC, UVA offload `--cpu-offload-gb 12.25` of the PLE n-gram table and input embeddings, `Q38_EXPERT_HOST_PLACEMENT` 3.5 GiB/rank) plus `VLLM_XPU_HC_TRITON=1` printed into the packet's derived launch source (the launcher strips inherited `VLLM_*` variables, so the flag lives in the packet, not the shell) |
| Full pins | [`identity.json`](identity.json) |

Evidence: [A306 realistic suite](../../experiments/qwen38-flash-next-fp8-b70/data/20260907-tp4-mtp1-a306-qsafused-realistic-suite-v1-result.json), [promotion attestation](../../experiments/qwen38-flash-next-fp8-b70/data/20260907-tp4-mtp1-a306-promotion-attestation.json),
[A305 battery summary](../../experiments/qwen38-flash-next-fp8-b70/data/20260907-tp4-mtp1-a305-fresh-repeat-deterministic-summary.json), [A297/A304/A305 exact-2K pair](../../experiments/qwen38-flash-next-fp8-b70/data/20260907-tp4-mtp1-qsafused-exact-2k-pair-summary.json),
[A266](../../experiments/qwen38-flash-next-fp8-b70/data/20260906-tp4-mtp0-a266-hctriton-screen-quality-current.json) / [A267](../../experiments/qwen38-flash-next-fp8-b70/data/20260906-tp4-mtp0-a267-hctriton-screen-fresh-quality-current.json) / [A268](../../experiments/qwen38-flash-next-fp8-b70/data/20260906-tp4-mtp1-a268-hctriton-screen-quality-current.json) quality screens,
[placement file](../../experiments/qwen38-flash-next-fp8-b70/data/20260906-q38-expert-host-placement-3p5gib-per-rank.json), [LocalMaxxing response](../../data/localmaxxing-responses/qwen38-flash-next-fp8-tp4-mtp1-placement-hctriton-realistic-20260907.json),
run-directory manifests [`evidence/a305-run.sha256`](evidence/a305-run.sha256) and [`evidence/a306-run.sha256`](evidence/a306-run.sha256).
The narrative is in the [result packet](../../results/qwen38-flash-next-fp8-b70/README.md).

## Dependency closure

| Component | Identity and link |
| --- | --- |
| Host platform | Ubuntu 24.04, Linux 7.0 xe driver, four B70s on one host; **no tested install path** (open gate) |
| Accelerator toolchain | oneAPI 2025.3 compiler runtime, `torch 2.11.0+xpu`, `triton 3.7.0`; venv contents recorded in [`pip-freeze-observed.txt`](../qwen38-flash-next-fp8-tp4-mtp3-b70/pip-freeze-observed.txt) (observed, not an installable hash lock; open gate) |
| Runtime source | public `76cfe1cd`, the [lossless-MTP1 series](../../patches/qwen38-flash-next-fp8-b70/vllm-lossless-mtp1-1b2a17c1/README.md) to `1b2a17c1`, the [placement series](../../patches/qwen38-flash-next-fp8-b70/vllm-placement-mtp1-005dc578/README.md) to `005dc578`, then the [Triton-HC series and bundle](../../patches/qwen38-flash-next-fp8-b70/vllm-qsafused-mtp1-6d872457/README.md) (`verify-series.sh --apply` re-creates tree `3e8dfc59…`) |
| Native kernels | hosted stage `2f829747` (hybrid build: only `_moe_C` freshly built at that head, [disclosure](../qwen38-flash-next-fp8-tp4-mtp3-b70/RELEASE-NOTES.md)) |
| Collective runtime | hosted public oneCCL `4ceafd1` build ([receipt](../../patches/qwen38-flash-next-fp8-b70/oneccl-4ceafd1-b70-public/README.md)) |
| Model | publisher revision `bcd9f01d`, [contract](../qwen38-flash-next-fp8-tp4-mtp3-b70/model-contract.json) and [`verify-model.py`](../qwen38-flash-next-fp8-tp4-mtp3-b70/verify-model.py) |
| Configuration | the frozen A306 packet (four scripts pinned by [`frozen-a306-packet.sha256`](frozen-a306-packet.sha256)) and the placement file; server line in [`container-serve.sh`](container-serve.sh) |
| Execution | `verify-identity.sh`, `run-record-gate.sh` (below); container route unbuilt |
| Verifier pin | the frozen packet pins the exactness verifier by bytes; [`verifier-pin.txt`](verifier-pin.txt) records its SHA-256, git blob and the last lab commit that carries it, and `verify-identity.sh` names that commit when the file has moved on |
| Last replay | 2026-09-07 15:56, attempt 307 through `run-record-gate.sh` on the originating host: 12/12 outputs identical to the record, every gate equal, 37.972404 tok/s class-balanced ([gate log](evidence/a307-record-gate.log), [run manifest](evidence/a307-record-gate-replay.sha256), [suite result](../../experiments/qwen38-flash-next-fp8-b70/data/20260907-tp4-mtp1-a307-record-gate-replay-realistic-suite-v1-result.json)) |
| Validation | frozen client: fixed cold realistic suite once, exactness verifier `verify-moe-m1-w13-n32-selection.py` (`c874852b…`), fresh-response gates; `check-replay-result.py` compares output pins and gates with the record |

## Restore source

```bash
cd /path/to/b70-optimization-lab
REPRO_VLLM_TREE=/path/to/vllm-clone patches/qwen38-flash-next-fp8-b70/vllm-lossless-mtp1-1b2a17c1/verify-series.sh --apply
REPRO_VLLM_TREE=/path/to/vllm-clone patches/qwen38-flash-next-fp8-b70/vllm-placement-mtp1-005dc578/verify-series.sh --apply
REPRO_VLLM_TREE=/path/to/vllm-clone patches/qwen38-flash-next-fp8-b70/vllm-qsafused-mtp1-6d872457/verify-series.sh --apply
git -C /path/to/vllm-clone checkout q38-hctriton-mtp1-62219122
```

The kernel stage and the oneCCL build are downloaded from their releases and
checked against the tracked manifests (`runtime-stage.sha256`, `lib.sha256`);
the mtp3 guide's frozen `prepare-runtime.py` installs the stage tar.

## Run

```bash
cd /path/to/b70-optimization-lab
repro/qwen38-flash-next-fp8-tp4-mtp1-qsafused-b70-38tps-20260907/verify-identity.sh
REPRO_ATTEMPT=<unused number above 272> repro/qwen38-flash-next-fp8-tp4-mtp1-qsafused-b70-38tps-20260907/run-record-gate.sh
```

`verify-identity.sh` checks, without touching the GPUs: the placement and
Triton-HC overlay bundles, tags, trees and patch series; the checked-out overlay
head and a clean tree; the 18 stage files; both oneCCL hashes; the model config,
safetensors index and shard count; the tuned map, the exactness verifier, the
frozen packet and the placement file; and the Python runtime versions. Defaults
are the originating host's paths; each of `REPRO_VLLM_TREE`,
`REPRO_KERNEL_STAGE`, `REPRO_ONECCL_ROOT`, `REPRO_MODEL_ROOT`, `REPRO_VENV_ROOT`
may point at the same verified artifacts elsewhere, and an absent default stops
with the variable's name.

`run-record-gate.sh` derives a fresh attempt from the frozen A306 packet
(`make-replay-attempt.py`: byte-identical apart from attempt number, port and
state names, internal hashes recomputed), runs the packet's own static
validation, launches it through the lab's host-controlled launcher (root:
swap and ASPM reset, page-cache drop, fail-closed preflight on processes,
ports, mounts and free space), waits for `/health`, sends the fixed cold
realistic suite once with the record's flags (the packet's frozen client is the
separate certification battery, A305, and is not re-run), stops the server
through the packet's stop file, and compares `realistic-suite-v1-result.json`
with the record: all 12 prompt and output SHA-256s must match and every gate
must equal the record's. The replay's class-balanced median is printed beside
37.825654 tok/s; speed is reported, not gated, because an exact replay that is
slower is still exact. A full pass takes about 25 minutes (9-12 minutes of
model load from the lab's USB copy, graph capture, the suite).

Stop: the packet's supervisor tears the server down at the end of the client
run and writes `/tmp/q38-mtp1-ple-only-a<N>.rc`; check that no `Worker_TP`
process or listener on the packet port remains.

## What is not certified

- no clean-host install: the venv, oneAPI runtime, xe driver and model copy
  are assumed; `pip-freeze-observed.txt` is a receipt, not a hash lock;
- non-originating-host replay: none yet; the host-controlled launcher assumes
  the lab's mounts and swap layout;
- container route: written, unbuilt, unreplayed ([status](CONTAINER-STATUS.md));
- the kernel stage is a hybrid build (only `_moe_C` rebuilt at `2f829747`), and
  the oneCCL binary is pinned by bytes, not by a reproducible build;
- the outputs are a new authority: they are deterministic and reproduced across
  servers, and the quality profile equals the certified torch-fallback rows, but
  they are not bit-identical to those rows; a consumer that pinned the
  `afffd211…` / `c6193cc6…` outputs must re-pin;
- the placement is a census artefact: experts never routed to on the exact-2K
  trajectory and the realistic suite; a workload that routes to a host-placed
  expert pays a PCIe read for that row (outputs unchanged within the lineage);
- the record is one measurement of one workload class (short/medium
  realistic prompts at 4,352 max length); long-context and concurrency behaviour
  are research, not part of this replay.

Ongoing optimization of this line continues in the
[experiment directory](../../experiments/qwen38-flash-next-fp8-b70/); nothing
there changes this packet until a new record is certified and catalogued.
