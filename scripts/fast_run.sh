#!/usr/bin/env bash
set -euo pipefail
N_EVID="${N_EVID:-200}"

# Track a cheap fingerprint of research corpus (excluding generated folders)
FP_FILE="/opt/atlas/memory/reports/research_fingerprint.txt"
NEW_FP="$(find /opt/atlas/research -type f \
  ! -path "*/_incoming/*" ! -path "*/_text/*" ! -path "*/_ocr/*" ! -path "*/_meta/*" \
  -printf "%p %s %T@\n" | sort | sha256sum | awk '{print $1}')"

OLD_FP="$(cat "$FP_FILE" 2>/dev/null || true)"

echo "[FP] new=$NEW_FP old=$OLD_FP"
if [ "$NEW_FP" != "$OLD_FP" ]; then
  echo "[CHANGE] research changed -> extract + harvest"
  python3 /opt/atlas/scripts/pdftext_all.py || true
  python3 /opt/atlas/scripts/harvest_text_passages.py || true
  echo "$NEW_FP" > "$FP_FILE"
else
  echo "[SKIP] no research changes -> skip extract/harvest"
fi

# Always run the light steps
python3 /opt/atlas/scripts/fill_toid_from_nakshatra_yaml.py || true
N_EVID="$N_EVID" python3 /opt/atlas/scripts/evidencefill_v2.py || true
python3 /opt/atlas/scripts/canon_build_strict.py || true
atlas factcheck || true
atlas seedgraph || true
