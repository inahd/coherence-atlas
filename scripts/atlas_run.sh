#!/usr/bin/env bash
set -euo pipefail
RUN_WGET="${RUN_WGET:-0}"
DOMAIN="${DOMAIN:-all}"
N_EVID="${N_EVID:-50}"
RUN_OCR="${RUN_OCR:-0}"

SNAP="$(/opt/atlas/scripts/snapshot.sh 2>/dev/null || true)"
[ -n "${SNAP:-}" ] && echo "[SNAPSHOT] $SNAP"

echo "[GAPS]"; atlas gaps || true
echo "[PICK]"; atlas pick || true
if [ -f /opt/atlas/memory/reports/next_domain.txt ]; then
  DOMAIN="$(cat /opt/atlas/memory/reports/next_domain.txt)"
fi
echo "[DOMAIN] $DOMAIN"

if [ "$RUN_WGET" = "1" ]; then
  echo "[WGET] $DOMAIN"; atlas wget_guarded "$DOMAIN" || atlas wgetcycle "$DOMAIN" || true
else
  echo "[WGET] skipped (set RUN_WGET=1)"
fi

python3 /opt/atlas/scripts/promote_incoming.py || true
python3 /opt/atlas/scripts/pdftext_all.py || true

if [ "$RUN_OCR" = "1" ] && [ -x /opt/atlas/scripts/ocr_lowtext.sh ]; then
  python3 /opt/atlas/scripts/find_lowtext_pdfs.py || true
  bash /opt/atlas/scripts/ocr_lowtext.sh || true
fi

python3 /opt/atlas/scripts/harvest_text_passages.py || true

atlas seed || true
atlas autolink || true
python3 /opt/atlas/scripts/evidencefill.py "$N_EVID" || true

atlas seedgraph || true
atlas aggregate || true
atlas dashboard || true
atlas factcheck || true

echo "[DONE] atlas run"
[ -n "${SNAP:-}" ] && echo "[ROLLBACK] /opt/atlas/scripts/rollback.sh $SNAP"
