# MiniMax M2.7 INT4: what the four-card host has to run

This lane cannot be measured on the two-B70 host (`steve-TURIND8-2L2T`). The AutoRound INT4 export is
about 115 GB of weights against 64 GiB of VRAM there, with 15 GiB of system RAM, so no offload path
makes it servable at a precision this lab would accept. Everything below therefore waits on the
four-B70 measuring host. Nothing here is speculative about the gap: it is a VRAM fact, not a policy.

What was finished off-host, on 2026-09-07:

- `manifests/model-pin.json` gained the publisher's 25 `lfs_files` SHA-256 digests
  (120,752,899,559 bytes) at the pinned revision, without widening the packet's `provenance_limit`.
  A future download can now be verified byte for byte even though the historical May run cannot.

## Where the weights are

The INT4 export and its vLLM caches were moved off the fast disk on 2026-09-07 to make room for the
Qwen3.5 lanes:

| what | where | size |
| --- | --- | ---: |
| model | `/media/steve/extended-ssd/model-cold-storage/minimax-m2.7` | 214 GB |
| vLLM caches | `/media/steve/extended-ssd/model-cold-storage/minimax-m2.7-vllm-caches` | 311 GB |

`/home/steve/llm-models/move-minimax-caches-to-usb.sh` recorded the move with a 522-line manifest.
Copy back to fast local storage before serving; the external SSD is not a serving-speed device.

## The gap between this lane and the current bar

The promoted result is `89.314` output tok/s at prompt 512 / output 1536, gated with exact token
hashes and semantic canaries. That was the standard at the time. The standard the Qwen3.5 lanes now
meet is stricter, and the difference is what a four-card session should close:

| gate | MiniMax today | current bar |
| --- | --- | --- |
| repeat identity across two fresh servers | not established | G1: two MTP0 servers exact, 12/12 |
| candidate pair identity | not established | G2: two speculative servers exact, 12/12 |
| candidate vs oracle | not established | G3: speculative vs same-configuration MTP0 oracle, 12/12 |
| concurrency identity | not established | ladder c1-c64 with `--require-output-identity` |
| long context | 32K endpoint baseline only | 2K-32K real-content ladder against an oracle |
| container packet | none | level-2 packet, compose generated from the launcher |

## Suggested order on the four-card host

1. Restore the weights to fast local storage and verify against `manifests/model-pin.json`
   (`repro/qwen38-27b-autoround-int4-b70/scripts/verify-model-direct.py` reads this schema).
2. Bring the service up with the existing, tested scripts in `scripts/` - they are the ones that
   produced the promoted result, and nothing in them was changed by this session.
3. Only then add gates. The Qwen3.5 harness
   (`experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-campaign.sh`) is the closest working
   model for strict pairs plus ladders, but it is written around the vLLM XPU launchers of the
   Qwen3.8 FP8 recipe and would need a MiniMax launcher wired in; it is a template, not a drop-in.
4. Speed work should target what the effort index already identified rather than flag sweeps: MoE
   output all-reduce plus epilogue, or attention `o_proj` all-reduce plus residual/RMSNorm fusion.

## One result from this session that transfers

The two-card Qwen3.5 lanes show output identity holding at every concurrency on one card and
breaking at high concurrency on two, on both the 4B and the 9B. The mechanism under test is that
XCCL's reduction order depends on message size, so a step's result depends on how many rows share
it. MiniMax is a four-card TP lane whose top speed target is the MoE all-reduce, so whatever comes
out of `experiments/qwen35-9b-b70/scripts/run-20260907-qwen35-9b-rowwise-allreduce-chain.sh` applies
here directly - both for the identity claim and for what an efficient collective would have to do.
