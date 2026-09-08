#!/usr/bin/env bash
# Replay this record's realistic-suite leg on the originating host.
#
# What it does: derives a fresh frozen packet from A301 with this record's one-line map
# change (W1_CONFIG.BLOCK_SIZE_N 64), verifies the identity pins, and runs the same cold
# suite the record used. It does not re-derive the record; it produces one more suite
# measurement of the same configuration, which is how A325, A326 and A333 were taken.
#
#   ATTEMPT=<n> PORT=<p> run-record-replay.sh
#
# ATTEMPT and PORT must be unused: the packet writes to a run directory named after the
# attempt, and reusing one would write into an existing run's directory.
set -Eeuo pipefail

readonly repo=/home/steve/llm-optimizations
readonly tools="$repo/experiments/qwen38-flash-next-fp8-b70/tools"
readonly overlay=2a372e860e273273357cb7437ac7de1694304f9f
readonly map="$repo/experiments/qwen38-flash-next-fp8-b70/configs/moe-m1-w13-n64/E=128,N=640,device_name=Intel(R)_Arc(TM)_Pro_B70_Graphics,dtype=fp8_w8a8,block_shape=[128,128].json"
readonly map_sha=4fcb5d13ef0c859d12a4fe6b5aac09b04fccf4db24e47a6f004d3f9878e4e38f

die() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
attempt="${ATTEMPT:?set ATTEMPT to an unused attempt number}"
port="${PORT:?set PORT to an unused port}"

[[ -f "$map" ]] || die "tuned map is missing: $map"
[[ "$(sha256sum "$map" | cut -d' ' -f1)" == "$map_sha" ]] \
  || die "tuned map drifted; this record is defined by that file"
head="$(git -C /home/steve/src/vllm-current-main rev-parse HEAD)"
[[ "$head" == "$overlay" ]] \
  || die "overlay head is $head, expected $overlay (git -C /home/steve/src/vllm-current-main checkout $overlay)"
ls "/mnt/usb-models/bench-results/qwen38-flash-next-fp8-b70/"*"attempt${attempt}" >/dev/null 2>&1 \
  && die "attempt ${attempt} already has a run directory; choose an unused number"

readonly src_gen="$tools/rewrite-q38-a301-to-a333-mtp0-w13-blockn64-suite-third.py"
readonly src_drv="$tools/q38-a333-suite-driver.sh"
[[ -f "$src_gen" ]] || die "packet generator is missing: $src_gen"
[[ -f "$src_drv" ]] || die "suite driver is missing: $src_drv"

work="$tools/rewrite-q38-a301-to-a${attempt}-mtp0-w13-blockn64-suite-replay.py"
drv="$tools/q38-a${attempt}-suite-driver.sh"
[[ -e "$work" || -e "$drv" ]] && die "attempt ${attempt} artefacts already exist; choose an unused number"

# Five renames, the same ones every packet in this lane derives by: the campaign slug, the
# run-directory attempt, the ATTEMPT env, the port, and the script names.
sed -e "s/a333/a${attempt}/g" -e "s/A333/A${attempt}/g" \
    -e "s/attempt333/attempt${attempt}/g" -e "s/ATTEMPT=333/ATTEMPT=${attempt}/g" \
    -e "s/\"19946\"/\"${port}\"/g" -e "s/ATTEMPT=301\", \"ATTEMPT=333/ATTEMPT=301\", \"ATTEMPT=${attempt}/" \
    "$src_gen" > "$work"
sed -e "s/333/${attempt}/g" -e "s/19946/${port}/g" "$src_drv" > "$drv"
chmod +x "$drv"

python3 "$work" >/dev/null || die "packet generation failed"
env "Q38_A${attempt}_REWRITE_VALIDATE_ONLY=1" python3 "$work" >/dev/null \
  || die "packet does not regenerate identically"
launcher="$tools/launch-tp4-mtp0-4352-ple-only-a${attempt}-fullgraphdet-w13n64.sh"
grep -q "ATTEMPT=${attempt} PORT=${port}" "$launcher" \
  || die "derived launcher does not carry ATTEMPT=${attempt} PORT=${port}; the rename did not take"
grep -q "moe-m1-w13-n64" "$launcher" || die "derived launcher lost the 64-wide map"

echo "packet derived and validated for attempt ${attempt} on port ${port}"
echo "the record's suites measured 34.510128 (A325), 34.495292 (A326, submitted) and"
echo "34.520093 (A333); their range is 0.0248, so a replay inside about 34.47-34.55"
echo "reproduces it. MTP0 is the quiet lineage -- one suite is enough here, unlike MTP1."
exec "$tools/q38-launch-frozen-attempt.sh" "$attempt" "$drv" /tmp/q38-attempt-logs
