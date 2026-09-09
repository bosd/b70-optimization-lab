# Targeted correctness cleanup — 2026-09-08

Scope: recent September 6–8 changes, existing repository validators and the
new [community PR #45](https://github.com/steveseguin/b70-optimization-lab/pull/45).
This was a bounded review, not a line-by-line audit of all 244 recent commits.
Commit author labels alone do not establish which model introduced a defect.

## Fixed

- `tools/container-packet/smoke-test.sh` compared shell-captured text, which
  strips trailing newlines. Different completions could therefore pass its
  exact-repeat gate. It now compares parsed JSON strings directly, rejects
  malformed/empty/non-string responses, propagates validation failure and
  writes a passing result only after successful comparison. The printed
  example now uses the configured served model rather than a hardcoded 9B ID.
- `.github/workflows/guides.yml` now runs manifest-path validation and the
  smoke regression tests, with triggers covering the validator and shared
  container scripts.
- PR #45's R50 classifier patch was imported with attribution and its original
  submission preserved. Actual-source CPU tests reproduce the shape-only
  prefill misclassification and verify the fix in both R50 source copies.
  A separate candidate image builds and passes the same tests from both
  working directories. Its [validation record](../community/dominick253-qwen38-27b-fp8-uniform-decode-alias/validation/README.md)
  contains identities, commands and the remaining model/soak gates.
- Corrected the contribution's claim that its patch includes a microbatch
  veto: it does not. Its illustrative test also cannot enforce failure via
  exit status; the added actual-source test does.

## Checks

- Eleven smoke/container-checker regression tests pass, using fake Docker and
  HTTP commands for the smoke test.
- Syntax checks pass for 130 tracked Python and 427 tracked shell files
  changed since September 6; experiment scripts were not executed.
- Claims (11), guides (38), document links (206 documents) and manifest paths
  (4,347 paths in 49 manifests) pass validation.
- Candidate build: 15 cases with stock/fixed expectations on each source copy;
  both copies pass again in fresh CPU-only containers after the build.

## Remaining limits

The pin audit reports 229 mismatches among 263 literal pins, all involving
two evolving Flash-Next verifier scripts referenced by frozen research
clients. These are pre-existing provenance/replay concerns, not permission
to replace recorded identities with today's hashes. No pins were rewritten.

No GPU/model regression or sustained soak was run for the classifier fix;
the contributor's multi-hour incident remains community-reported. No live
model service was found during this review or started by it. Original images,
promoted scores and the three pre-existing dirty Qwen3.5 probe/script files
were preserved.
