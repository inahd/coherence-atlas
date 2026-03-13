#!/usr/bin/env bash
set -euo pipefail

# Controls
RUN_WGET="${RUN_WGET:-0}"
RUN_OCR="${RUN_OCR:-0}"          # 0/1 (OFF by default)
N_EVID="${N_EVID:-50}"             # evidencefill rows per cycle
DOMAIN_OVERRIDE="${DOMAIN_OVERRIDE:-}"  # if set, forces a domain

LOG="/opt/atlas/logs/cycle_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

echo "[START] $(date) RUN_WGET=$RUN_WGET RUN_OCR=$RUN_OCR N_EVID=$N_EVID DOMAIN_OVERRIDE=$DOMAIN_OVERRIDE"

# Snapshot if available
if [ -x /opt/atlas/scripts/snapshot.sh ]; then
  SNAP="$(/opt/atlas/scripts/snapshot.sh)"
  echo "[SNAPSHOT] $SNAP"
else
  SNAP=""
  echo "[SNAPSHOT] skipped (missing snapshot.sh)"
fi

# Gap scoring + choose next domain
python3 /opt/atlas/scripts/gap_score.py
python3 /opt/atlas/scripts/pick_manifest.py

DOMAIN="$(cat /opt/atlas/memory/reports/next_domain.txt 2>/dev/null || echo nakshatra)"
if [ -n "$DOMAIN_OVERRIDE" ]; then
  DOMAIN="$DOMAIN_OVERRIDE"
fi
echo "[DOMAIN] $DOMAIN"

# Optional wget acquisition
if [ "$RUN_WGET" = "1" ]; then
  echo "[WGET] atlas wgetcycle $DOMAIN"
  atlas wgetcycle "$DOMAIN" || true
else
  echo "[WGET] skipped (set RUN_WGET=1 to enable)"
fi

# Promote new incoming (if present)
if [ -f /opt/atlas/scripts/promote_incoming.py ]; then
  echo "[PROMOTE] promote_incoming.py"
  python3 /opt/atlas/scripts/promote_incoming.py || true
fi

# PDF -> text
if [ -f /opt/atlas/scripts/pdftext_all.py ]; then
  echo "[PDFTEXT] pdftext_all.py"
  python3 /opt/atlas/scripts/pdftext_all.py || true
fi

# Optional OCR for low-text PDFs
if [ "$RUN_OCR" = "1" ]; then
  echo "[OCR] scanning low-text PDFs"
  python3 /opt/atlas/scripts/find_lowtext_pdfs.py || true
  echo "[OCR] running OCR on low-text PDFs"
  bash /opt/atlas/scripts/ocr_lowtext.sh || true
else
  echo "[OCR] skipped (set RUN_OCR=1 to enable)"
fi


# Harvest passages from _text
if [ -f /opt/atlas/scripts/harvest_text_passages.py ]; then
  echo "[HARVEST] harvest_text_passages.py"
  python3 /opt/atlas/scripts/harvest_text_passages.py || true
fi

# Seed + autolink + evidencefill
echo "[SEED] atlas seed"
atlas seed || true

echo "[AUTOLINK] atlas autolink"
atlas autolink || true

if [ -f /opt/atlas/scripts/evidencefill.py ]; then
  echo "[EVIDENCEFILL] $N_EVID"
  python3 /opt/atlas/scripts/evidencefill.py "$N_EVID" || true
fi

# Seed graph rebuild
echo "[SEEDGRAPH] atlas seedgraph"
atlas seedgraph || true

# Factcheck report
echo "[FACTCHECK] atlas factcheck"
atlas factcheck || true

echo "[DONE] $(date)"
echo "[LOG] $LOG"
if [ -n "$SNAP" ]; then
  echo "[ROLLBACK] /opt/atlas/scripts/rollback.sh $SNAP"
fi
