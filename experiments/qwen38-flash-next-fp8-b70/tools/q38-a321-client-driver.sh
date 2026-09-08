#!/usr/bin/env bash
# A321's driver: the readiness wrapper bound to the MTP0 W13-N64 screen's frozen client.
set -Eeuo pipefail
d=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec "$d/q38-client-driver.sh" 321 19991 mtp0 "$d/run-tp4-mtp0-4352-ple-only-a321-fullgraphdet-w13n64-client.sh"
