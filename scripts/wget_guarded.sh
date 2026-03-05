#!/usr/bin/env bash
set -euo pipefail

DOMAIN="${1:-nakshatra}"   # domain tag only; maps to manifest file
MANIFEST="/opt/atlas/manifests/wget_${DOMAIN}.txt"
OUTROOT="/opt/atlas/research/_incoming/${DOMAIN}"
LOG="/opt/atlas/logs/wget_guarded_${DOMAIN}_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$OUTROOT" /opt/atlas/logs

if [ ! -f "$MANIFEST" ]; then
  echo "Missing manifest: $MANIFEST"
  exit 1
fi

# optional allowlist file: one domain per line (e.g., gretil.sub.uni-goettingen.de)
ALLOW="/opt/atlas/manifests/allow_domains.txt"

echo "[WGET GUARDED] domain=$DOMAIN manifest=$MANIFEST out=$OUTROOT" | tee -a "$LOG"

# Extract hostnames from manifest and enforce allowlist if file exists
if [ -f "$ALLOW" ]; then
  bad=0
  while IFS= read -r url; do
    [[ "$url" =~ ^# ]] && continue
    [ -z "$url" ] && continue
    host="$(python3 - <<PY
from urllib.parse import urlparse
import sys
u=sys.argv[1]
print(urlparse(u).hostname or "")
PY
"$url")"
    if ! grep -qxF "$host" "$ALLOW"; then
      echo "[BLOCKED] $host not in allowlist" | tee -a "$LOG"
      bad=1
    fi
  done < "$MANIFEST"
  [ "$bad" = "1" ] && { echo "Allowlist violation. Fix /opt/atlas/manifests/allow_domains.txt"; exit 1; }
fi

# wget options:
# --wait: sleep between downloads
# --random-wait: jitter
# --limit-rate: keep polite
# --robots=on: respect robots.txt
# --user-agent: identify
wget -i "$MANIFEST" \
  -P "$OUTROOT" -nc --content-disposition \
  --timeout=30 --tries=3 --no-verbose \
  --wait=2 --random-wait --limit-rate=800k \
  --robots=on --user-agent="AtlasResearchBot/0.1 (+local)" \
  2>&1 | tee -a "$LOG" || true

echo "[DONE] $LOG"
