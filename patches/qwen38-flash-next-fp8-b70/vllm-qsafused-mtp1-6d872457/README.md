# Qwen3.8 Flash-Next fused QSA pre-indexer on the Triton-HC MTP1 head (`6d872457`)

Exported: 2026-09-07

The second of two reference restorations. The XPU port of this model replaced two of the
model's own Triton kernels: the hyper-connection glue (restored in
`../vllm-hctriton-mtp1-62219122/`) and the QSA pre-indexer, which ran as an unfused
sequence of qk projection, query norm and rope, group compression, compressed-key norm
and rope, and two or three cache-row stores. A per-phase timing split put projection and
compression at 18.0 of the indexer's 23.9 ms per eager step. This series runs the model's
reference fused kernel (`nvidia/ops/qsa_pre_indexer.py`, plain Triton) on XPU instead,
behind `VLLM_XPU_QSA_FUSED_INDEXER=1`, on top of the Triton-HC MTP1 head `62219122`.
The MTP0 twin is `q38-qsa-fused` at `2a372e86` (the same two commits on `8d7d6fd8`,
tree `a3e420fc…`).

The second patch matters for correctness rather than speed: on the MTP1 head the
multi-row verification step takes `_forward_serial_rows`, which exists so that rows
sharing a compression group cannot race for one compressed slot, and the fused branch
must sit after it rather than replace it.

**This line is a new output authority, and the change is at depth.** Exact-2K coincides
with the certified stream (`afffd211…`) while exact-4K does not (`1d833e5f…` in place of
`c6193cc6…`). What it preserves is the quality profile, byte for byte against the
certified battery: seven of seven exact-case outputs identical, sixteen repeats collapsing
to one hash, the long-context needle identical. Within the lineage MTP1 stays lossless,
reproducing the MTP0 pins at both depths. LocalMaxxing approved
[`cmtrmp3mj001fps01thcathd0`](https://www.localmaxxing.com/runs/cmtrmp3mj001fps01thcathd0)
at 37.825654 tok/s with one speculative token, and
[`cmtrmp37v001bps01a7fi46nf`](https://www.localmaxxing.com/runs/cmtrmp37v001bps01a7fi46nf)
at 33.797067 without.

- base: `622191221475b53cc6f7f4d847860939f4c300ab` (restore from the Triton-HC bundle first);
- head: `6d8724577dabbee5fa0bbc70c4d927c6174c8d8a`, tree `3e8dfc5937087d186cd4a99a6bf15213be732462`;
- bundle `vllm-q38-qsafused-mtp1-6d872457-20260907.bundle` carries tag `q38-qsafused-mtp1-6d872457`;
- `series.sha256` pins both patches and the bundle; `verify-series.sh --apply` re-creates the tree.

| Patch | Subject |
| --- | --- |
| `0001-XPU-VLLM_XPU_QSA_FUSED_INDEXER-1-run-the-reference-f.patch` | [XPU] VLLM_XPU_QSA_FUSED_INDEXER=1: run the reference fused QSA pre-indexer on XPU |
| `0002-XPU-the-fused-QSA-pre-indexer-must-not-preempt-the-r.patch` | [XPU] the fused QSA pre-indexer must not preempt the row-serial verify path |

```bash
REPRO_VLLM_TREE=/path/to/vllm-clone patches/qwen38-flash-next-fp8-b70/vllm-qsafused-mtp1-6d872457/verify-series.sh --apply
```
