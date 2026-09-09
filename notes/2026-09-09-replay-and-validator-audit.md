# Replay and validator correctness audit

Scope: risk-prioritized review of reusable tooling changed September 6–8,
2026. Commit author labels do not establish which model authored a change.
This is not certification that every recent experiment is free of bugs.

## Corrections

- `tools/check-container-packet.py` did not compare serving arguments between
  its one-card and two-card profiles despite documenting that invariant.
  It now allows only the tensor-parallel flag's value to differ; mutation
  tests reject a changed context limit or an extra serving flag.
- `tools/audit-launcher-env-implemented.py` interpreted Docker failure or
  incomplete output as evidence that every forwarded variable was inert.
  Both now fail without producing a successful variable audit. The container
  scan also rejects absent site-packages, missing grep, and grep read errors;
  grep's ordinary no-match status remains valid.
- The promoted Flash-Next lossless, placement and Triton-HC recipes pinned
  historical versions of a shared verifier that had subsequently changed.
  Each recipe now includes `verify-moe-selection-frozen.py`, extracted from
  its original recorded Git blob and matching its unchanged `verifier-pin.txt`
  SHA-256. Identity checks use that snapshot, and generated replay clients
  redirect both their hash check and invocation to it. Their supervisor hashes
  are recomputed by the existing generator. Original frozen clients, verifier
  pins, result identities and the evolving shared verifier remain intact.
  The fused-QSA recipe already matched the current shared verifier.
- All four Flash-Next MTP1 replay drivers could skip their STOP request when
  the benchmark failed under `set -e`. An EXIT trap now requests the owned
  server's stop while preserving the benchmark exit status. Tests execute
  each actual driver with mocked endpoint/process commands for success and
  failure (eight cases).

These are tooling repairs, not new model-quality or throughput measurements.
The publication skill guided dependency closure: all three historical
snapshots are package dependencies and the generated catalog was refreshed.
No public performance claim or generated model page changed.

## Bundle provenance repair

The first broad test run found four September 6–7 Flash-Next bundles missing
from the portability inventory: lossless `1b2a17c1`, placement `005dc578`,
Triton-HC `62219122`, and fused-QSA `6d872457`. All are thin bundles, including
the first, whose README incorrectly called it complete-history. That claim
is corrected.

Their exact reconstruction chain was verified in a disposable bare repository:
fetch public vLLM commit `76cfe1cd88d30d525eec8be5bff75f8b77471c88`, then
restore the four original bundles in the order above. The new
`manifest-backed-tracked-chain` classification records the HTTPS base and
its tree, every bundle path and SHA-256, each prerequisite, advertised ref,
tip and tree. Offline checks reject missing, reordered, duplicate, tampered,
misdirected or cyclic steps. Public validation additionally fetches the
base, verifies and restores each bundle, checks exact tips/trees and ancestry,
and runs Git object-connectivity validation. Existing classifications and the
53-entry frozen legacy allowlist are unchanged.

The four `.provenance.json` files alongside these bundles preserve this
ordered recovery declaration. The inventory now has 58 bundles: 53 frozen
legacy artifacts and five manifest-backed entries. A live proof of the
four-step chain passed using only the public base and tracked bundle bytes;
none of the owning host's source checkout was used as the restoration base.

Run the complete inventory's offline guard with:

```bash
python3 tools/validate-git-bundle-inventory.py --inventory data/git-bundle-portability-inventory-v1.json
```

Add `--verify-public-remotes` for live restoration proofs, including the
existing unrelated public-prerequisite bundle. The completed live check in
this review specifically exercised the four-step Flash-Next chain.

## Validation

- Tools suite: 163 tests passed after repairing the bundle-inventory failure
  (including the separate GPU-health probe regressions added during review).
- `scripts/` tests: 118 passed; `scripts/tests/`: 45 passed.
- Three container packets pass the strengthened checker.
- Guide validation: 38 guides valid. Manifest paths: 4,353 checked, none
  missing. Markdown links: 207 documents checked, none broken.
- All three historical snapshots match their original SHA-256 pins; tests
  also reject tampering, verify both client references are redirected, and
  confirm all historical hash tokens survive the redirection unchanged.
- Model page generation produced no tracked page difference; `git diff
  --check` passes. New regressions are included in the guides CI workflow.

## Remaining limits

The literal hash scanner still reports 229 historical experimental-client
mismatches involving the evolving N16/N32 validators. Those frozen experiments
were not blanket-repinned. The scanner does not resolve variable-held hashes;
its total alone cannot certify promoted recipes. The three promoted replay
paths above now use their own historical copies.

Semantic source review additionally covered the shared container smoke,
download, preflight and verify scripts; Compose renderer and render wrapper;
the recent changes to the concurrency-oracle, long-context and realistic-suite
benchmark harnesses; and the historical replay generator/identity/driver paths
described above. Source inspection and mocked tests do not establish real
GPU runtime correctness. The Flash-Next recipes require four cards and were
not launched on this two-card host. The separate PR #45 GPU validation record
owns its own actual runtime results.

Existing dirty Qwen3.5 experiment work was preserved. No runtime services,
GPU workloads or model files were modified by this audit.
