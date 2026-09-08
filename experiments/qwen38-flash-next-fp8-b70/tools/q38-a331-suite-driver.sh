#!/usr/bin/env bash
# A331's driver: replay of the Triton-HC lossless-MTP1 suite record.
set -Eeuo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/q38-suite-driver.sh" 331 19944 mtp1
