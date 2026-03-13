#!/usr/bin/env bash
set -euo pipefail
cd /opt/atlas
source /opt/atlas/venv/bin/activate
python3 /opt/atlas/scripts/pb_state.py
python3 /opt/atlas/scripts/pb_emit.py
echo ""
echo "===== NEXT PASTEBLOCK (copy/paste) ====="
cat /opt/atlas/memory/reports/next_pasteblock.sh
