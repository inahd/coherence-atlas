#!/usr/bin/env bash
set -euo pipefail
SNAP="${1:-}"
if [ -z "$SNAP" ] || [ ! -f "$SNAP" ]; then
  echo "Usage: rollback.sh /opt/atlas/backups/snap_YYYYMMDD_HHMMSS.tgz"
  exit 1
fi
tar -xzf "$SNAP" -C /
echo "[ROLLED BACK] $SNAP"
