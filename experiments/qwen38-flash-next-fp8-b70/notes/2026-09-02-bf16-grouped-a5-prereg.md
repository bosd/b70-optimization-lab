# Flash-Next BF16 grouped-W16A16 A5 preregistration

Date: 2026-09-02
Status: frozen before device execution

## Objective

A4a showed that the global deterministic provider control is exact overall but
fails same-row native-support parity only for four `K=10240` down-projection
cells. A5 asks the cheapest decisive follow-up: does the already built Xe2
grouped W16A16 provider return one stable, natively supported BF16 result for
each of those cells? This is a component-only test. It cannot change an
endpoint, protected output, speed claim, or quality claim.

The tool is
[`census-q38-bf16-grouped-a5.py`](../tools/census-q38-bf16-grouped-a5.py),
SHA-256
`df1655c7ca35a5e7f225d408e5040aef0c95a381069c0d13fc9f4e8ff7ae14f9`.
Its focused tests are
[`test_census_q38_bf16_grouped_a5.py`](../tools/test_census_q38_bf16_grouped_a5.py),
SHA-256
`84fe3edf9df1cfea06185a7159332f246c86cf20970ca1913f0cb27e603c4270`.
The machine-readable contract is
[`20260902-bf16-grouped-a5-prereg.json`](../data/20260902-bf16-grouped-a5-prereg.json).

## Frozen authority and scope

The input/weight authority is the A1 real-checkpoint loader at SHA-256
`e4700fc44a65d71c7b0a7df5ff34924d808ba685c4157b0e2c12fd4b9d4bdf22`.
Same-row output support comes only from the immutable A4a native records under
the complete summary SHA-256
`a98b7c7f34df9795027e1e7b956fde8daef485986f9de31d96813b4c98c6d6d2`.
The A5 tool binds all eight native-record hashes rather than trusting an
unversioned directory. The grouped runtime is the existing
`hc-grouped-stage-eeee7d6-sycl8` stage, whose manifest SHA-256 is
`71e263f19ccc1313bbdc21604b4de5171891454fb7e8e35877af083505522951`;
every listed runtime file is verified before use.

The four cells are:

| Cell | Family / sentinel | Shape | Active/tail | Calls/token |
|---:|---|---|---|---:|
| 0 | `hc_down_inject` / `layer00-attn-r0` | M1 K10240 N352 | 0:324 active, 324:352 zero | 96 |
| 1 | `hc_down_inject` / `layer47-mlp-r3` | M1 K10240 N352 | 0:324 active, 324:352 zero | 96 |
| 2 | `final_hc_down` / `final-r0` | M1 K10240 N320 | all active | 1 |
| 3 | `final_hc_down` / `final-r3` | M1 K10240 N320 | all active | 1 |

For HC down, A1 reconstructs logical N336 with its known exact-zero 12-column
tail. A5 preserves the 324 active checkpoint columns and rebuilds the physical
candidate as N352 with 28 exact-zero columns, satisfying the grouped kernel's
N-divisible-by-32 contract. The final down weights are already N320 and need no
padding.

## Stage 1: parity before timing

Each cell gets two fresh sequential grouped-provider processes: eight processes
total. Each process independently loads its real sentinel weight and constructs
the same 256 distinct BF16 input rows with seed `2026090201`. After four
unreported complete-order warmup sweeps, it records 100 complete ordinal sweeps,
each consisting of 256 M1 calls.

A cell passes only if all of the following hold:

1. every process has one physical D hash and every row has one active hash;
2. both processes return the same physical D hash and the same active hash for
   every row;
3. each candidate row hash is present in that exact ordinal row's union of 200
   frozen A4a native observations;
4. every HC padded-tail value is exact numeric zero; and
5. source, runtime, input, logical weight, grouped weight, environment, and
   health identities remain exact.

The classifier also binds the exact cell schema, status, classification,
cell/family/sentinel/provider identity, replica set `{1,2}`, shape, protocol,
credit block, environment, and complete runtime manifest. The candidate's
aggregate input hash and all 256 input-row hashes must equal the frozen A4a
authority. Duplicate replicas, swapped cells, or internally inconsistent
compressed digest sets are therefore bounded negatives rather than eligible
evidence.

All four cells must pass. Timing captured during this stage is screening-only
and cannot rescue a parity failure.

Execution requires `Q38_BF16_GROUPED_A5_EXECUTE=YES`. The new no-clobber root
is:

`/mnt/usb-models/bench-results/qwen38-flash-next-fp8-b70/bf16-grouped-down-20260902-a5`

## Conditional stage 2: N/G/G/N timing bracket

Stage 2 is frozen, not implemented or authorized by this change. It becomes
eligible only when the preserved stage-1 summary says all eight processes and
all four parity cells passed. It uses a separate no-clobber root:

`/mnt/usb-models/bench-results/qwen38-flash-next-fp8-b70/bf16-grouped-down-timing-20260902-a5b`

Each cell then receives four fresh processes in exact native-1, grouped-1,
grouped-2, native-2 order. Parity is rechecked before timing interpretation.
The preregistered report-only cost screen weights HC down by 96 calls/token and
final down by one: central grouped/native must be at most 1.000, each family at
most 1.020, and the two native controls may drift by at most 1.030. A pass still
authorizes only a separately preregistered serving integration candidate.

## Safety and interpretation

The harness selects one B70, holds the existing exclusive component lock,
checks admission before and after each child, and writes atomically without
replacement. Final admission and the across-plan AER comparison occur before
`summary.json` is constructed or published. A final-admission exception or a
late AER event writes `failure.json`, including a second final-health attempt,
and leaves no passing summary. Stage-1 and stage-2 evidence paths are disjoint from A4a and the
concurrent W13 builder lane. The change performs no model-server launch, full
model load, reboot, source/runtime edit, endpoint change, or GPU execution by
itself. A negative result closes this provider for these four cells; a positive
result advances only to the conditional timing bracket.
