#!/usr/bin/env bash
# Check that this machine can run the packet before anything is downloaded or started.
# Reports every finding, then exits non-zero if any hard requirement failed.
#   PROFILE  one-gpu (default) or two-gpu
set -uo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd); pkg=$(cd -- "${here}/.." && pwd)
profile=${PROFILE:-one-gpu}
need_cards=1; [[ "${profile}" == two-gpu ]] && need_cards=2
digest=$(grep -m1 '^  image:' "${pkg}/compose.yaml" | awk '{print $2}')
fail=0; warn=0
ok()   { printf '  ok    %s\n' "$*"; }
bad()  { printf '  FAIL  %s\n' "$*"; fail=1; }
note() { printf '  note  %s\n' "$*"; warn=1; }

printf 'Qwen3.5-9B W4A16 B70 packet preflight (profile: %s)\n\n' "${profile}"

printf 'runtime\n'
command -v docker >/dev/null && ok "docker $(docker --version | awk '{print $3}' | tr -d ,)" || bad "docker is required"
docker compose version >/dev/null 2>&1 && ok "docker compose $(docker compose version --short 2>/dev/null)" || bad "the docker compose plugin is required"
docker info >/dev/null 2>&1 && ok "docker daemon reachable" || bad "cannot talk to the docker daemon (is the user in the docker group?)"

printf '\ngpu\n'
cards=$(ls /dev/dri/renderD* 2>/dev/null | wc -l)
if command -v xpu-smi >/dev/null 2>&1; then
  intel=$(xpu-smi discovery 2>/dev/null | grep -c 'Device Name: Intel(R) Arc(TM) Pro B70')
  normal=$(xpu-smi discovery 2>/dev/null | grep -c 'Device State: normal')
  [[ "${intel}" -ge "${need_cards}" ]] && ok "${intel} Arc Pro B70 present (need ${need_cards})" || bad "${intel} Arc Pro B70 present, this profile needs ${need_cards}"
  [[ "${normal}" -ge "${need_cards}" ]] && ok "${normal} device(s) in normal state" || bad "a device is not in normal state; check xpu-smi discovery"
else
  note "xpu-smi not installed; falling back to render node count"
  [[ "${cards}" -ge "${need_cards}" ]] && ok "${cards} render node(s) (need ${need_cards})" || bad "${cards} render node(s), this profile needs ${need_cards}"
fi
[[ -e /dev/dri ]] && ok "/dev/dri present" || bad "/dev/dri is missing; the Intel GPU driver is not loaded"
id -nG 2>/dev/null | tr ' ' '\n' | grep -qx render && ok "user is in the render group" || note "user is not in the render group; the container adds it, but host tools may not see the GPU"
drvname=$( [[ -d /sys/module/xe ]] && echo xe || { [[ -d /sys/module/i915 ]] && echo i915 || echo none; } )
drvver=$(cat "/sys/module/${drvname}/version" 2>/dev/null || true)
[[ "${drvname}" == none ]] && bad "neither the xe nor the i915 kernel driver is loaded" \
  || ok "kernel graphics driver: ${drvname}${drvver:+ ${drvver}}"

printf '\nmemory and storage\n'
ram=$(free -g | awk '/^Mem:/{print $2}')
[[ "${ram}" -ge 12 ]] && ok "${ram} GiB system RAM" || note "${ram} GiB system RAM; the container is limited to 12g and may need swap"
model_dir=${MODEL_DIR:-}
if [[ -n "${model_dir}" && -d "${model_dir}" ]]; then
  ok "MODEL_DIR exists: ${model_dir}"
else
  target=$(dirname -- "${model_dir:-$PWD/model}")
  avail=$(df -BG --output=avail "${target}" 2>/dev/null | tail -1 | tr -dc '0-9')
  if [[ -n "${avail}" ]]; then
    [[ "${avail}" -ge 12 ]] && ok "${avail} GiB free at ${target} (model needs ~11 GiB)" || bad "${avail} GiB free at ${target}; the model needs about 11 GiB"
  else
    note "could not measure free space; the model needs about 11 GiB"
  fi
fi

printf '\nimage\n'
if docker image inspect "${digest}" >/dev/null 2>&1; then
  ok "image present: ${digest}"
else
  note "image not present locally; pull it with:  docker pull ${digest}"
fi

printf '\n'
if [[ "${fail}" == 1 ]]; then printf 'preflight FAILED\n'; exit 1; fi
[[ "${warn}" == 1 ]] && printf 'preflight passed with notes\n' || printf 'preflight passed\n'
