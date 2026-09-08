#!/usr/bin/env bash
# A312's driver: the generic exact-depth diagnostic driver bound to this packet's
# attempt, port and speculation depth (the frozen-attempt launcher takes a bare path).
set -Eeuo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/q38-exact-depth-driver.sh" 312 19982 mtp1
