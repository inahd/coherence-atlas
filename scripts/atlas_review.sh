#!/usr/bin/env bash
set -euo pipefail
N_STAGE="${N_STAGE:-200}"
N_AUTO="${N_AUTO:-150}"
MIN_SCORE="${MIN_SCORE:-2.5}"
N_EXPORT="${N_EXPORT:-80}"

SNAP="$(/opt/atlas/scripts/snapshot.sh 2>/dev/null || true)"
[ -n "${SNAP:-}" ] && echo "[SNAPSHOT] $SNAP"

atlas corpus_init || true
atlas corpus_scan || true
atlas corpus_pdftext || true
atlas corpus_harvest || true

atlas stage "$N_STAGE" || true
atlas autoapply "$N_AUTO" "$MIN_SCORE" || true
atlas promote_auto_export "$N_EXPORT" || true

echo "[REVIEW] edit: /opt/atlas/staging/promote_auto_preview.csv"
${EDITOR:-nano} /opt/atlas/staging/promote_auto_preview.csv

atlas promote_auto_apply || true
atlas seedgraph || true
atlas factcheck || true
atlas dashboard || true

echo "[DONE] atlas review"
[ -n "${SNAP:-}" ] && echo "[ROLLBACK] /opt/atlas/scripts/rollback.sh $SNAP"
