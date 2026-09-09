# PR45 remaining-wall localization plan — September 9

Historical reproduction on the exact already-tested R50 candidate, not new
active-upstream optimization. No promoted configuration or quality gate changes.

1. Before server localization, run the existing complete production-shape
   W8A16 census and repeat-determinism sweep, including the actual FP16 head.
   Skip the census's nonproduction FP8 head and later R99-specific auxiliary
   implementations absent from R50. Record every shape and negative result.
2. Audit one-token prefill dispatch and speculative metadata at source level.
   Classifier guard alone is known insufficient. Integer-token API requests
   must remain intact; no padding or prompt substitution may count as a fix.
3. Based on the operator/source evidence, preregister a minimal target-only
   versus MTP control or isolated state-path correction, using fresh servers,
   identical tiny/mixed probes, clean caches and exact image identities.
4. Only a candidate that clears the unchanged screen advances to full strict
   quality/canaries and fresh-server repeats. No performance promotion from
   diagnostics. Long-session soak remains a later gate, not a substitute for
   resolving the immediate reproducible failure.

Every device run owns bounded health checks, exclusive lock, new output path
and cleanup. Abort on infrastructure or kernel fault; preserve failures.

## Control preregistered after operator census

The six W8A16 projection shapes and actual FP16 head completed. R50's known
large-M nondeterminism remains (four W8A16 projections, starting at M=168),
while repeated M=1..4 was stable and row zero matched across M=1..4. This
clears those tested operators only for the immediate tiny-shape discriminator,
not general batch invariance or model correctness.

Run `candidate-target-only`: identical to the previous compilation-disabled
candidate screen, except `SPECULATIVE_CONFIG=null`. Same 24 requests and
64-token cap; a repetition failure is retained. If it also fails, MTP is not
required for this local symptom. Independently inspect GDN's fresh-one-token
prefill routing, including capture metadata and mixed batches, before any patch.

## GDN phase-guard campaign

The target-only control failed 3/24 probes. A distinct GDN splitter classified
fresh one-token prompts as decode and read existing conv/SSM state. The worker
zeroing helper skips Mamba layers. The local candidate routes phase-aware short
prefills to prefill kernels; metadata-less draft/capture callers retain their
existing behavior. Eight actual-source splitter/call cases pass stock/fixed
against both source copies. No prompt, model or numerical kernel is changed.

Candidate image:
`sha256:334c353ffc543eaea2de85d25d947ab5a0db36b9cfa043d0ed7d849627662e81`.
Build: `Dockerfile.gdn`, based on the earlier classifier-patched candidate.
This is maintainer follow-up, not part of the submitted classifier patch.

Preregistered order: `gdn-target-only` (same no-compile/no-MTP control with only
this new image), then `gdn-mtp`, then `gdn-mtp-repeat` on fresh servers/caches.
Both MTP arms retain the original compiled strict profile and full quality
suite, with the unchanged 24-request screen before and after that suite.
Every failed screen or infrastructure check aborts remaining arms. Compare
complete normal-suite token arrays to the prior baseline and between fresh
candidate runs. No speed or long-soak claim follows from this short campaign.
