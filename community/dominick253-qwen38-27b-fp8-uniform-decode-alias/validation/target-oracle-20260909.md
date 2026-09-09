# Remaining target-oracle matrix

Preregistered: two fresh `gdn-target-strict` / `gdn-target-strict-repeat`
servers using the existing GDN phase-guard image and compiled strict profile.
Only speculation changes to `null`; model, precision, prompts, cache policy,
quality thresholds and output cap stay fixed. Existing supervisor owns the
pre/post tiny screens, complete 12-prompt suite, canaries, teardown and health.

Compare both target runs to each other and to both already-recorded compiled
MTP runs. Every complete token array must match; any failed comparison blocks
promotion and the six-hour soak. No performance tuning or production change.

Results: **passed**. Both fresh target-only runs passed full workload/cache-zero
and canary gates, plus all 96 pre/post tiny/mixed probes. Target-to-target and
all four target-to-MTP comparisons match 12/12 complete output token arrays.
The [five-comparison matrix](target-oracle-20260909/matrix.json) and complete
run evidence are retained in the adjacent directory. Both servers stopped;
both GPUs/XCCL and kernel postflights passed. No soak or promotion performed.

Raw run root:
`/mnt/fast-ai/bench-results/pr45-target-oracle-20260909`.
