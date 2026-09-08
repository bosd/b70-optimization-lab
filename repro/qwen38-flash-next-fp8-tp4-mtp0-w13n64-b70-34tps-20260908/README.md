# Reproduce the Qwen3.8 Flash-Next MTP0 record: 34.495292 tok/s on four Arc Pro B70

This is the lab's fastest **non-speculative** line for Qwen3.8 Flash-Next FP8 on
four Intel Arc Pro B70s, and it differs from the record it supersedes by a single
line of a tuned configuration file.

| | superseded | this record |
| --- | --- | --- |
| class-balanced median | 33.797067 tok/s (A301) | **34.495292 tok/s** (A326) |
| first suite | — | 34.510128 (A325) |
| LocalMaxxing run | `cmtrmp37v001bps01a7fi46nf` | `cmts8zca50032ps01e0ddqm18` |
| W13 phase tile | `BLOCK_SIZE_N: 32` | `BLOCK_SIZE_N: 64` |

Twelve fresh rows in each suite, `cached_tokens` zero throughout, and every row of
both new suites is above every row of the superseded one.

## What changed, and what did not

One line of `configs/moe-m1-w13-n64/E=128,N=640,…json`:

```
-      "BLOCK_SIZE_N": 32
+      "BLOCK_SIZE_N": 64
```

That sets the W13 phase tile equal to the base tile, so the per-phase delta resolves
to the same value the GEMM would have used anyway and stops doing anything. **No
source change**: 64 was already an allowed tile, so the certified overlay head
`2a372e86` runs unmodified and the published configuration is strictly simpler than
the one it replaces.

The delta had been adopted in A56 (2026-09-02) bundled with the eight-warp M1 change
— "(eight-warp M1 and W13-N32) therefore compose into a real endpoint gain" — and the
two were never separated. The warp count carries that gain; the tile did not.

## Why it is lossless

A phase delta resolves only at batch size 1, and this line decodes at 1
(`cudagraph_capture_sizes: [1]`, no speculation), so the tile is the decode tile.
Changing which output columns a program owns leaves every output element's K loop
identical, and the server agrees: across A321, A322 and A323 on three separate
servers, six exact-2K rows and six exact-4K rows all carry the certified stream's
hashes, `afffd2110812…` and `1d833e5f4633…`.

`evidence/record-evidence.sha256` pins the two suite results, the promotion
attestation, both three-server lossless summaries and the submitted payload.

## The tile ladder, measured in the server

| W13 `BLOCK_SIZE_N` | 16 | 32 | **64** | 128 |
| --- | --- | --- | --- | --- |
| exact-2K tok/s | 31.39 (A320) | 33.38 (A304) | **34.15** (A321/2/3) | 26.29 (A327) |

The ladder has an optimum and this record sits on it. An offline kernel probe ranked
these tiles differently — it put 16 ahead of 32 and 64, and the server ran 16 six
percent slower — so tiles on this kernel are ranked in the server or not at all. The
same probe put 128 last and was right about that, so it is unreliable in both
directions rather than reliably inverted.

## Run it

The frozen packets are pinned in `frozen-a325-a326-packets.sha256`; the tuned map and
its selection verifier in `verifier-and-map-pin.txt`. The procedure, the dependency
closure and the restore-source steps are identical to the MTP1 sibling guide
(`repro/qwen38-flash-next-fp8-tp4-mtp1-qsafused-b70-38tps-20260907/README.md`),
which this line shares a stage, a oneCCL build and a torch pin with; the differences
are the overlay head (`2a372e86`), `MTP=0`, and the tuned config folder
(`moe-m1-w13-n64`).

Verify the map selection before running:

```
python3 experiments/qwen38-flash-next-fp8-b70/tools/verify-moe-m1-w13-n64-selection.py \
  --base-config-file      experiments/qwen38-flash-next-fp8-b70/configs/moe-warps8-m1/E=128,N=640,…json \
  --candidate-config-file experiments/qwen38-flash-next-fp8-b70/configs/moe-m1-w13-n64/E=128,N=640,…json \
  --vllm-source <overlay checkout at 2a372e86> \
  --phase-config-patch patches/qwen38-flash-next-fp8-b70/vllm/0021-Add-opt-in-per-phase-Triton-MoE-configs.patch \
  --output /tmp/receipt.json
```

It must report `status pass`, key 1, W13 `BLOCK_SIZE_N` 64 with W2 64, and every
preservation check true — the last of which proves that all integer batch sizes from
2 to 512 still resolve exactly as the retained map does.

## What is not certified

- **The container route.** Not provided; see `CONTAINER-STATUS.md` for why, and for
  the torch-ABI blocker it shares with the MTP1 guide.
- **MTP1.** The same change is a *regression* there: −0.066 tok/s across four rows
  (A324), because MTP1 verifies two positions, decodes at batch 2 where the delta is
  dropped regardless, and the only path the delta still reaches is the separately
  captured draft head, which prefers 32. The MTP1 record is unchanged and keeps its
  delta.
- **Anything about the model's weights or outputs.** This record's stream is
  bit-identical to the one it supersedes.

## When a run fails

Every failure below was hit while producing or replaying this record on 2026-09-08, with the
symptom as it actually appears. None is hypothetical.

**The launcher exits `FAIL: swap still in use after reset:  bytes`.** The preflight refuses to
start while swap is in use, and the byte count is empty because the previous server was still
releasing its pinned host memory (12.8 GiB per rank here). Wait for the previous attempt's
`.rc` file to appear, confirm `/proc/swaps` shows `0` used, and relaunch. Retrying immediately
just reproduces it.

**The launcher exits `FAIL: vLLM overlay head changed`.** The packet pins its overlay commit
and does not check it out for you. `git -C /home/steve/src/vllm-current-main checkout <head>`
first — for this record, `2a372e86`.

**The server never becomes healthy, and the log ends in repeated `No available shared memory
broadcast block found in 60 seconds`.** This is usually *not* a hang. After graph capture the
API server takes about two and a half minutes to bind, and that message repeats while it does.
Confirm with `curl -fsS http://127.0.0.1:<port>/health`; if the workers are idle at ~47 W and
`Graph capturing finished` is in the log, wait. I mistook this for a stall once and confirmed
it was healthy only by dumping the Python stacks with `py-spy dump --pid <worker>`, which
showed every process parked in its normal wait loop.

**Weight loading crawls — 15 s/shard instead of 1–4, projecting 30+ minutes.** The launcher
drops the page cache before every run, so each attempt re-reads ~185 GB from the USB mount and
that mount's read rate varies a lot between runs. It recovers on its own; a second load pass
at 6+ it/s off warm cache is normal and is not a restart.

**A worker dies with `Caught signal 11` inside `libucs.so.0` during weight loading.** Seen once
(A330). `dmesg` showed `Engine reset: engine_class=ccs` on one card; the driver recovered it
and all four cards enumerated normally afterwards. It did not recur across the four following
runs. Check `dmesg | grep -c "Engine reset"` before and after — if the count is unchanged on a
retry, it was transient and the retry is the right response.

**The client aborts after every leg with an `AssertionError` and no message.** The frozen
client's final block pins output hashes; if one belongs to a different lineage the assertion
fires with no explanation. Check which authority the packet expects against what the run
produced — `exact-depth-*.json` carries `output_token_ids_sha256`. This is what A323 hit, and
it was the pin that was wrong, not the run.

**`FAIL: W13-N64 selection verifier drifted`.** The client pins the selection verifier by hash
and the verifier is shared, mutable tooling. Run `python3 tools/check-pinned-hashes.py` to see
whether the pin or the file moved. Do not re-pin a frozen packet to make it pass: the pin is
part of what the packet attests.

**Before blaming the recipe, check the host.** `xpu-smi discovery` should list four cards;
`xpu-smi dump -d 0,1,2,3 -m 0,1 -n 1` should show ~45 W idle and rise under load. A packet
cannot fix a card that is not there.
