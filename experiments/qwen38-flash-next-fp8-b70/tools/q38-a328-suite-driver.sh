#!/usr/bin/env bash
# A328's driver: replay of the certified lossless-MTP1 suite record.
set -Eeuo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/q38-suite-driver.sh" 328 19998 mtp1
