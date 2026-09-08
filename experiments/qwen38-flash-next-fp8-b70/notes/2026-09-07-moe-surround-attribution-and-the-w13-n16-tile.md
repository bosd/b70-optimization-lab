# Where the MoE step's time goes, and a 16-wide W13 tile that was never measured

With A314 closing the host-placement lever, the cards were free, so this is an offline
attribution of the MoE step at decode shape (M=1, 128 local experts, K=2560, N=640,
top-k 10), timing each stage of `fused_experts_impl` under graph replay of 48 layers.

| stage | per layer | share |
| --- | --- | --- |
| gemm1 (W13) | 77.26 µs | 64.3% |
| gemm2 (W2) | 27.62 µs | 23.0% |
| assign (`moe_align_block_size`) | 6.30 µs | 5.2% |
| reduce (`moe_sum`) | 3.13 µs | 2.6% |
| quantize1 | 2.42 µs | 2.0% |
| quantize2 | 2.25 µs | 1.9% |
| activation | 1.13 µs | 0.9% |

**The surround is not the lever.** Everything that is not a GEMM comes to 15.2 µs per layer,
0.73 ms across 48 layers. Even if the server's 3.2 ms of surround is real, at most a quarter
of it is work these kernels do; the rest is not something a faster kernel removes. Fusing
them is not worth the risk to exactness.

**The W13 tile is.** W13 is about two thirds of the modelled step, and its N tile is the one
knob that does not touch arithmetic — the N tile decides which output columns a program
owns, and leaves every output element's K loop identical. Sweeping it:

| W13 BLOCK_N | per layer |
| --- | --- |
| **16** | **69.08 µs** |
| 32 (certified) | 77.30 µs |
| 64 | 91.98 µs |

10.6% off the dominant kernel. The other directions are already at their best: W2's N sweep
picks the certified 64 (27.6 µs against 36.5 at 16, 43.3 at 32, 62.3 at 128), num_warps=8
beats 4 and 16 by ~35%, and num_stages does not matter.

**It was tried this morning and never measured.** A291 loaded `configs/moe-m1-w13-n16` at
10:39 and all four workers died in startup at 10:50 with

```
ValueError: W1_CONFIG.BLOCK_SIZE_N must be one of [32, 64, 128, 256]
```

The per-phase config patch validates the tile against an allowlist that omits 16. The run
produced no artifacts, so the lever was blocked by a validator rather than by the hardware,
which runs the tile fine — the probe above uses it.

**Exactness.** The argument from the K loop is not enough on its own, because `tl.dot` may
take a different path through the systolic array for a [16, 16] tile than a [16, 32] one,
and the order of the reduction inside one dot is not fixed by the kernel source. So the two
tilings were compared elementwise over 300 fresh random decode cases: **zero differing
elements of 3,840,000**. That is the same screen that caught the swapped accumulator layout
when a three-call version had missed it (A290), so it is worth something — but the server's
exact-2K hash remains the test of record.

**A317** is the screen: the fused-QSA MTP1 identity with the tile as its only change, on
head `a9115342`, which widens the allowlist and nothing else. Its exact-depth rows compare
against A305's 38.981 / 38.972 (2K) and 39.299 / 39.304 (4K).

## Evidence

- `tools/probe-moe-surround-decode-offline.py` — the attribution above.
- `tools/screen-moe-w13-blockn16-equality-offline.py` — the 300-case equality screen.
- `data/20260907-tp4-mtp0-a291-blockn16-validator-reject.log` — the validator that blocked it.
- Packet: `tools/rewrite-q38-a311-to-a317-mtp1-w13-blockn16-screen.py`.
