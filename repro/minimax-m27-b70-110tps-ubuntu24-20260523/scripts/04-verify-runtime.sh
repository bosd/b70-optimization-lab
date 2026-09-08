#!/usr/bin/env bash
set -euo pipefail

THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$THIS_DIR/configs/runtime-env.sh"
source "$VENV/bin/activate"
# Intel's vars.sh dereferences SETVARS_CALL and OCL_ICD_FILENAMES, which are unbound when
# it is sourced directly, so under `set -u` it aborts -- and with both streams muted the
# abort is silent. It also *replaces* LD_LIBRARY_PATH rather than prepending, which drops
# the venv's torch libraries and leaves torch.xpu.device_count() at 0 on a machine with
# four working cards. So: relax -u for the vendor script only, fail loudly if it fails, and
# re-apply the search path runtime-env.sh set before it.
_q38_ld_before="${LD_LIBRARY_PATH:-}"
set +u
source /opt/intel/oneapi/compiler/2025.3/env/vars.sh >/dev/null 2>&1 || {
  echo "FAIL: could not source the oneAPI compiler environment" >&2; exit 1; }
set -u
export LD_LIBRARY_PATH="${_q38_ld_before}${_q38_ld_before:+:}${LD_LIBRARY_PATH:-}"
unset _q38_ld_before

python - <<'PY'
import torch
from vllm.platforms import current_platform
import vllm
import vllm_xpu_kernels
import custom_esimd_kernels_vllm.moe_int4_ops as moe

print("platform", current_platform.device_type)
print("torch", torch.__version__, torch.xpu.is_available(), torch.xpu.device_count())
print("vllm", vllm.__version__)
print("vllm_xpu_kernels", getattr(vllm_xpu_kernels, "__version__", "ok"))
print("moe_int4_ops", moe.__name__)
assert current_platform.device_type == "xpu"
assert torch.xpu.is_available()
assert torch.xpu.device_count() == 4
PY

xpu-smi discovery
clinfo -l

