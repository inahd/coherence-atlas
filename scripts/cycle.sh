#!/usr/bin/env bash
set -euo pipefail

N_EVID="${1:-25}"

SNAP="$(/opt/atlas/scripts/snapshot.sh)"
echo "[SNAPSHOT] $SNAP"

# download step optional: uncomment when manifests have real urls
# /opt/atlas/scripts/wget_cycle.sh all
python /opt/atlas/scripts/promote_incoming.py
python /opt/atlas/scripts/pdftext_all.py
python /opt/atlas/scripts/harvest_text_passages.py

# keep your existing seed/autolink/factcheck tools
atlas seed || true
atlas autolink || true

python /opt/atlas/scripts/evidencefill.py "$N_EVID"

atlas seedgraph || true

echo "[DONE] cycle completed. If you dislike results, rollback with:"
echo "  /opt/atlas/scripts/rollback.sh $SNAP"
