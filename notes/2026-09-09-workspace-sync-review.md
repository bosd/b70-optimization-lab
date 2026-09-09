# Workspace sync and local-change review

Fast-forwarded main from `156241ad6` to `cd8541d96`. At entry, the main
repository had no uncommitted changes, stashes, or unpushed commits.
Commit author names do not establish which model wrote a change.

Reviewed incoming shared-tooling and replay changes and inventoried recent
dirty files and upstream-ahead commits in immediate `/home/steve/src`
checkouts, plus the community checkout. No recent upstream-ahead commits
were found against their locally configured tracking refs (runtime remotes
were not fetched).

The recent `/home/steve/src/vllm` compatibility shim is now preserved at
[`minimax-shared-expert-gate-compat-20260908.patch`](../patches/minimax-shared-expert-gate-compat-20260908.patch).
Base commit: `44fc8fde09fc311d3099dab10366b672d9142ea4`.
It accepts the always-forwarded `shared_expert_gate=None` argument and rejects
an actual gate because this runner cannot apply it. Rationale and failed
bring-up evidence remain in
[`the original note`](2026-09-08-minimax-bringup-four-fixed-faults-and-a-wedged-driver.md).
This is a source snapshot, not a runtime correctness or performance promotion.

The recent MiniMax record checkout's tracked diff and three untracked files
match the older boundary checkout; that stack is already preserved in
`repro/minimax-m27-b70-89tps-20260520/patches/vllm-active-promoted-minimax-89tps-20260520.patch.gz.b64`.
The community checkout is clean. Historical runtime deltas and ignored
experiment artifacts were preserved; no runtime checkout was edited.

Validation: 172 tools tests, 118 scripts tests, and 45 scripts/tests tests
passed (335 total). All 36 incoming Python/shell files passed syntax checks.
Guide, local publication, family generation, public-summary, container-packet,
document-link, manifest-path and 58-bundle offline inventory checks passed.
Model page regeneration produced no tracked changes.

The literal hash scanner still reports the previously documented 229
historical experiment pin mismatches; see the
[prior audit](2026-09-09-replay-and-validator-audit.md#remaining-limits).
Incoming whitespace warnings are confined to preserved patch context and raw
logs. No GPU workloads, service changes, remote publication proofs or fresh
model-quality benchmarks were run in this review.
