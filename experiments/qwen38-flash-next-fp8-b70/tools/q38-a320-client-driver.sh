#!/usr/bin/env bash
# A320's driver: the readiness wrapper bound to the MTP0 W13-N16 screen's frozen client.
set -Eeuo pipefail
d=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec "$d/q38-client-driver.sh" 320 19990 mtp0 "$d/run-tp4-mtp0-4352-ple-only-a320-fullgraphdet-w13n16-client.sh"
