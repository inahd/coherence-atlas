#!/usr/bin/env bash
set -euo pipefail

# Optional: set DO_PULL=1 to git pull; default 0 (no network changes)
DO_PULL="${DO_PULL:-0}"

SNAP=""
if [ -x /opt/atlas/scripts/snapshot.sh ]; then
  SNAP="$(/opt/atlas/scripts/snapshot.sh)"
  echo "[SNAPSHOT] $SNAP"
fi

echo "[TEST] pre"
bash /opt/atlas/scripts/run_tests.sh

if [ "$DO_PULL" = "1" ]; then
  echo "[GIT] pull"
  cd /opt/atlas
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 && git pull --rebase || echo "[WARN] not a git repo"
fi

echo "[TEST] post"
if ! bash /opt/atlas/scripts/run_tests.sh; then
  echo "[FAIL] tests failed after update"
  if [ -n "$SNAP" ] && [ -x /opt/atlas/scripts/rollback.sh ]; then
    echo "[ROLLBACK] $SNAP"
    /opt/atlas/scripts/rollback.sh "$SNAP"
  fi
  exit 1
fi

echo "[OK] safeupdate complete"
