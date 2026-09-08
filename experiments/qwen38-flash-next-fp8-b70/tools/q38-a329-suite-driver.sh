#!/usr/bin/env bash
# A329's driver: second replay of the certified lossless-MTP1 suite record.
set -Eeuo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/q38-suite-driver.sh" 329 19999 mtp1
