#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${1:-nakshatra}"           # nakshatra|tithi_nitya|ritual|music|plants|all
OUTROOT="/opt/atlas/research/_incoming"
LOG="/opt/atlas/logs/wget_cycle_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$OUTROOT" "/opt/atlas/logs"

download_list () {
  local list="$1"
  local tag="$2"
  local outdir="$OUTROOT/$tag"
  mkdir -p "$outdir"
  echo "[WGET] list=$list tag=$tag out=$outdir" | tee -a "$LOG"

  # -nc: no clobber, keep existing
  # --content-disposition: respect server filenames
  # --timeout/--tries: fail reasonably
  # --no-verbose: cleaner logs
CLEAN_LIST="$(mktemp)"
grep -vE '^[[:space:]]*(#|$)' "$LIST" > "$CLEAN_LIST"
trap 'rm -f "$CLEAN_LIST"' EXIT

  wget -i "$list" -P "$outdir" -nc --content-disposition --timeout=30 --tries=3 --no-verbose 2>&1 | tee -a "$LOG" || true
}

case "$DOMAIN" in
  nakshatra)   download_list "/opt/atlas/manifests/wget_nakshatra.txt"   "nakshatra" ;;
  tithi_nitya) download_list "/opt/atlas/manifests/wget_tithi_nitya.txt" "tithi_nitya" ;;
  ritual)      download_list "/opt/atlas/manifests/wget_ritual.txt"      "ritual" ;;
  music)       download_list "/opt/atlas/manifests/wget_music.txt"       "music" ;;
  plants)      download_list "/opt/atlas/manifests/wget_plants.txt"      "plants" ;;
  all)
    download_list "/opt/atlas/manifests/wget_nakshatra.txt"   "nakshatra"
    download_list "/opt/atlas/manifests/wget_tithi_nitya.txt" "tithi_nitya"
    download_list "/opt/atlas/manifests/wget_ritual.txt"      "ritual"
    download_list "/opt/atlas/manifests/wget_music.txt"       "music"
    download_list "/opt/atlas/manifests/wget_plants.txt"      "plants"
    ;;
  *) echo "Usage: wget_cycle.sh [nakshatra|tithi_nitya|ritual|music|plants|all]" ; exit 1 ;;
esac

echo "[DONE] $LOG"
