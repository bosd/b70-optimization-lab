#!/usr/bin/env bash
# A324's driver: the MTP1 W13-N64 screen's frozen client (A305's, on the 64-wide map).
set -Eeuo pipefail
d=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec "$d/q38-client-driver.sh" 324 19994 mtp1 "$d/run-tp4-mtp1-4352-ple-only-a324-fullgraphdet-w13n64-client.sh"
