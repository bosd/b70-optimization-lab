# 224 of 243 frozen clients cannot be re-run, because they pin a verifier that moved

Found while building A330, a replay of the Triton-HC MTP1 record: the generator asserted the
current verifier hash was present in A272's client and it was not. A272 pins `20546ff1…`;
the file is `c874852b…` today.

## The shape of it

Every frozen client gates itself on the W13-N32 selection verifier by hash:

```bash
[[ "$(sha256sum ".../verify-moe-m1-w13-n32-selection.py" | cut -d' ' -f1)" == <pinned> ]] || {
  printf 'FAIL: W13-N32 selection verifier drifted\n' >&2; exit 1; }
```

The packets are frozen. The verifier is shared and mutable — it gains accepted overlay heads
and per-head source hashes as lineages land. Every edit therefore invalidates the *forward*
re-runnability of every packet frozen before it.

| | count |
| --- | --- |
| clients pinning the verifier | 243 |
| pinning a hash that is no longer current | **224** |
| of those, ones that did run their client at the time | 13 |

The 13 (a72, a73, a78, a79, a120, a121, a187, a190, a223, a224, a225, a269, a271) passed
against the verifier as it stood on their day. **Their results are not in question.** What is
in question is whether anyone can run those clients again, and today they cannot: they abort
immediately on the drift check.

## Why this has stayed invisible

The records that matter are suite-driven. A272, A301 and A306 never ran their own clients —
their run directories hold `realistic-suite-v1-result.json` and nothing else — so the
replays that validate them (A328, A329, A330) never touch the pin. The exposure only appears
when someone reaches for a frozen *client*, which is exactly what happened to me twice
tonight: A323 aborted on A301's stale exact-4K authority pin, and A330's generator tripped on
A272's stale verifier pin.

## What this is and is not

It is **not** a reason to distrust published numbers. Each was gated by the contemporaneous
verifier, and the suite evidence behind the records is independent of the client path.

It is a real limit on reproduction: "frozen packet" means frozen against its own contents,
not against the shared tooling it points at. A reader handed one of those 224 clients cannot
run it without either restoring the verifier to its pinned state or editing the packet, and
editing the packet changes what its own hash chain refers to.

## What would fix it, and what I have not done

The clean fix is to make the verifier immutable per lineage — version the file
(`verify-moe-m1-w13-n32-selection-<sha>.py`) so a packet's pin always resolves — rather than
editing one shared file. That is a change to how the lane freezes packets, affecting 243
clients and their hash chains, and it is not something to do unilaterally at 04:00 while runs
are in flight. Recorded here for a deliberate decision.

The near-term rule already in memory stands: freeze the verifier before generating a batch of
packets, and regenerate any outstanding ones after an edit.

## Evidence

- Audit: for each `tools/run-tp4-mtp*-ple-only-a*-client.sh`, the pinned verifier hash
  against `sha256sum tools/verify-moe-m1-w13-n32-selection.py`, cross-referenced with whether
  the attempt's run directory contains `client-gates-passed.txt`.
- Instances hit in practice: `notes/2026-09-08-a323-a-third-confirmation-and-a-latent-pin-defect.md`
  (A301's exact-4K authority), and this note (A272's verifier).
