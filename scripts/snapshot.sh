#!/usr/bin/env bash
set -euo pipefail
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="/opt/atlas/backups/snap_$STAMP.tgz"
tar -czf "$OUT" \
  /opt/atlas/datasets \
  /opt/atlas/memory/graphs \
  /opt/atlas/research/_text \
  /opt/atlas/datasets/sources || true
echo "$OUT"
