#!/usr/bin/env bash
# A314's driver: the readiness wrapper bound to this packet's attempt, port, speculation
# depth and frozen client (the frozen-attempt launcher takes a bare path).
set -Eeuo pipefail
d=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec "$d/q38-client-driver.sh" 314 19984 mtp1 "$d/run-tp4-mtp1-4352-ple-only-a314-fullgraphdet-w13n32-client.sh"
