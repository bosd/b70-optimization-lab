#!/usr/bin/env bash
# A325's driver: the realistic-suite leg, which is how the published MTP0 figure was produced.
set -Eeuo pipefail
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/q38-suite-driver.sh" 325 19995 mtp0
