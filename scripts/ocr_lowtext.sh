#!/usr/bin/env bash
set -euo pipefail

LIST="/opt/atlas/research/_ocr/lowtext_pdfs.txt"
OUTTXT="/opt/atlas/research/_text"
TMP="/opt/atlas/research/_ocr/_tmp"

mkdir -p "$OUTTXT" "$TMP"

need() { command -v "$1" >/dev/null 2>&1 || { echo "MISSING: $1"; exit 1; }; }

# Required tools (install via distro):
# - poppler-utils (pdftoppm)
# - tesseract
need pdftoppm
need tesseract

if [ ! -f "$LIST" ]; then
  echo "No lowtext list found. Run: python3 /opt/atlas/scripts/find_lowtext_pdfs.py"
  exit 1
fi

n=0
while IFS= read -r pdf; do
  [ -z "$pdf" ] && continue
  base="$(basename "$pdf")"
  stem="${base%.*}"
  echo "[OCR] $base"

  rm -rf "$TMP/$stem"
  mkdir -p "$TMP/$stem"

  # render pages
  pdftoppm -png -r 200 "$pdf" "$TMP/$stem/page" >/dev/null 2>&1 || { echo "[FAIL] render $base"; continue; }

  # OCR each page image -> accumulate
  out="$OUTTXT/$stem.txt"
  : > "$out"
  for img in "$TMP/$stem"/page-*.png; do
    [ -f "$img" ] || continue
    # tesseract outputs to stdout with "stdout"
    tesseract "$img" stdout -l eng 2>/dev/null >> "$out" || true
    echo -e "\n\n" >> "$out"
  done

  chars=$(wc -c < "$out" || echo 0)
  echo "[OCR DONE] $base -> $out ($chars chars)"
  n=$((n+1))
done < "$LIST"

echo "[DONE] OCR processed $n PDFs"
