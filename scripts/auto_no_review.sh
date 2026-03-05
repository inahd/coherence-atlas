#!/usr/bin/env bash
set -euo pipefail

N_STAGE="${N_STAGE:-400}"
N_AUTO="${N_AUTO:-300}"
N_PROMOTE="${N_PROMOTE:-80}"
MIN_SCORE="${MIN_SCORE:-3.0}"

echo "[CFG] N_STAGE=$N_STAGE N_AUTO=$N_AUTO N_PROMOTE=$N_PROMOTE MIN_SCORE=$MIN_SCORE"

SNAP="$(/opt/atlas/scripts/snapshot.sh 2>/dev/null || true)"
if [ -n "${SNAP:-}" ]; then
  echo "[SNAPSHOT] $SNAP"
else
  echo "[SNAPSHOT] skipped"
fi

mkdir -p /opt/atlas/datasets/{relations_auto,relations}

atlas corpus_init || true
atlas stage "$N_STAGE" || true
atlas autoapply "$N_AUTO" "$MIN_SCORE" || true

# Auto-promote high-score staged/accepted rows directly into datasets/relations/
MIN_SCORE="$MIN_SCORE" N_PROMOTE="$N_PROMOTE" python3 - <<'PY'
import csv, sqlite3, os
from pathlib import Path

DB = Path("/opt/atlas/memory/corpus.db")
CANON = Path("/opt/atlas/datasets/relations")
CANON.mkdir(parents=True, exist_ok=True)

HDR = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"]

def ensure(p: Path):
    if not p.exists():
        with p.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HDR)

def append(p: Path, rows):
    ensure(p)
    existing=set()
    with p.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            existing.add((r.get("from_id",""), r.get("relation",""), r.get("to_id","")))
    added=0
    with p.open("a", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=HDR)
        for r in rows:
            k=(r["from_id"], r["relation"], r["to_id"])
            if k in existing:
                continue
            w.writerow(r)
            added += 1
    return added

min_score = float(os.environ.get("MIN_SCORE", "3.0"))
limit = int(os.environ.get("N_PROMOTE", "80"))

con = sqlite3.connect(DB)
cur = con.cursor()

cur.execute(
    "SELECT id,from_id,relation,to_id,source_sha256,locator,excerpt,score "
    "FROM staged_relations "
    "WHERE status IN ('accepted','staged') AND score>=? "
    "ORDER BY score DESC LIMIT ?",
    (min_score, limit)
)
rows = cur.fetchall()

total_added = 0
promoted_ids = []
for rid, fr, rel, to, sha, loc, ex, sc in rows:
    if not (fr and rel and to and sha and loc and ex):
        continue
    out = CANON / (rel.replace(":", "_") + ".csv")
    row = {
        "from_id": fr,
        "relation": rel,
        "to_id": to,
        "source_title": sha,
        "source_locator": loc,
        "excerpt": ex[:900],
        "tradition": "unknown",
        "confidence": "attested_secondary",
        "notes": f"AUTO_PROMOTED score={sc}"
    }
    total_added += append(out, [row])
    promoted_ids.append(rid)

for rid in promoted_ids:
    cur.execute("UPDATE staged_relations SET status='applied' WHERE id=?", (rid,))

con.commit()
con.close()

print(f"auto-promote: candidates={len(rows)} written_rows={total_added} -> {CANON}")
PY

atlas guard || echo "[WARN] atlas guard failed; see /opt/atlas/memory/reports/canon_guard.json"
atlas seedgraph || true
atlas dashboard || true

echo "[DONE] auto_no_review"
if [ -n "${SNAP:-}" ]; then
  echo "[ROLLBACK] /opt/atlas/scripts/rollback.sh $SNAP"
fi
