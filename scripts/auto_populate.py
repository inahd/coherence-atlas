import csv, sqlite3
from pathlib import Path

DB = Path("/opt/atlas/memory/corpus.db")
AUTO_DIR = Path("/opt/atlas/datasets/relations_auto")
CANON_DIR = Path("/opt/atlas/datasets/relations")
STAGING = Path("/opt/atlas/staging")
AUTO_DIR.mkdir(parents=True, exist_ok=True)
CANON_DIR.mkdir(parents=True, exist_ok=True)
STAGING.mkdir(parents=True, exist_ok=True)

HDR = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"]

def ensure_csv(path: Path):
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HDR)

def append_rows(path: Path, rows):
    ensure_csv(path)
    existing=set()
    with path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            existing.add((r.get("from_id",""), r.get("relation",""), r.get("to_id","")))
    added=0
    with path.open("a", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=HDR)
        for r in rows:
            key=(r["from_id"], r["relation"], r["to_id"])
            if key in existing:
                continue
            w.writerow(r)
            added += 1
    return added

def autoapply(n=100, min_score=2.5):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "SELECT id,from_id,relation,to_id,source_sha256,locator,excerpt,score "
        "FROM staged_relations WHERE status='staged' AND score>=? "
        "ORDER BY score DESC LIMIT ?",
        (min_score, n)
    )
    rows = cur.fetchall()

    by_file={}
    for rid, f, rel, t, sha, loc, ex, sc in rows:
        out = AUTO_DIR / (rel.replace(":", "_") + ".csv")
        by_file.setdefault(out, []).append({
            "from_id": f, "relation": rel, "to_id": t,
            "source_title": sha, "source_locator": loc, "excerpt": ex[:900],
            "tradition": "unknown", "confidence": "auto_proposed",
            "notes": f"AUTOAPPLY score={sc}"
        })

    total_added=0
    for out, rs in by_file.items():
        total_added += append_rows(out, rs)

    for rid, *_ in rows:
        cur.execute("UPDATE staged_relations SET status='accepted' WHERE id=?", (rid,))
    con.commit(); con.close()
    print(f"autoapply: accepted_candidates={len(rows)} written_rows={total_added} into {AUTO_DIR}")

def export_promote_preview(n=50):
    preview = STAGING / "promote_auto_preview.csv"
    with preview.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["src_file","from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes","promote(yes/no)"])
        count=0
        for p in sorted(AUTO_DIR.glob("*.csv")):
            with p.open(newline="", encoding="utf-8") as rf:
                for r in csv.DictReader(rf):
                    if count >= n: break
                    w.writerow([p.name, r["from_id"], r["relation"], r["to_id"], r["source_title"], r["source_locator"],
                                r["excerpt"], r.get("tradition","unknown"), r.get("confidence","auto_proposed"),
                                r.get("notes",""), "no"])
                    count += 1
            if count >= n: break
    print("Wrote:", preview)

def apply_promote_preview():
    preview = STAGING / "promote_auto_preview.csv"
    if not preview.exists():
        raise SystemExit("Missing preview: " + str(preview))

    promoted=0
    with preview.open(newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            if (r.get("promote(yes/no)") or "").strip().lower() != "yes":
                continue
            rel = r["relation"]
            out = CANON_DIR / (rel.replace(":", "_") + ".csv")
            ensure_csv(out)
            row = {
                "from_id": r["from_id"], "relation": rel, "to_id": r["to_id"],
                "source_title": r["source_title"], "source_locator": r["source_locator"], "excerpt": r["excerpt"],
                "tradition": r.get("tradition","unknown"),
                "confidence": "attested_secondary",
                "notes": (r.get("notes","") + " | PROMOTED_FROM_AUTO").strip(" |")
            }
            promoted += append_rows(out, [row])
    print(f"promote_auto: promoted_rows={promoted} into {CANON_DIR}")

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv)>1 else ""
    if cmd == "autoapply":
        autoapply(int(sys.argv[2]) if len(sys.argv)>2 else 100,
                  float(sys.argv[3]) if len(sys.argv)>3 else 2.5)
    elif cmd == "export":
        export_promote_preview(int(sys.argv[2]) if len(sys.argv)>2 else 50)
    elif cmd == "apply":
        apply_promote_preview()
    else:
        print("Usage:")
        print("  python3 auto_populate.py autoapply [N] [MIN_SCORE]")
        print("  python3 auto_populate.py export [N]")
        print("  python3 auto_populate.py apply")
