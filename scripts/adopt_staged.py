import csv, sqlite3, sys
from pathlib import Path

DB = Path("/opt/atlas/memory/corpus.db")
OUTDIR = Path("/opt/atlas/staging")
OUTDIR.mkdir(parents=True, exist_ok=True)

CANON = Path("/opt/atlas/datasets/relations/nakshatra__deity.csv")
HDR = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"]

def export_batch(limit=50):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "SELECT id,from_id,relation,to_id,source_sha256,locator,excerpt,score FROM staged_relations "
        "WHERE status='staged' ORDER BY score DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    con.close()

    out = OUTDIR / "adopt_preview.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id","from_id","relation","to_id","source_sha256","locator","excerpt","score","approve(yes/no)","tradition","confidence","notes"])
        for r in rows:
            w.writerow(list(r) + ["no","unknown","attested_secondary",""])
    print("Wrote:", out)

def apply_preview():
    preview = OUTDIR / "adopt_preview.csv"
    if not preview.exists():
        print("Missing preview:", preview)
        return

    con = sqlite3.connect(DB)
    cur = con.cursor()

    CANON.parent.mkdir(parents=True, exist_ok=True)
    if not CANON.exists():
        with CANON.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(HDR)

    existing=set()
    with CANON.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            existing.add((r.get("from_id",""), r.get("relation",""), r.get("to_id","")))

    applied=0
    with preview.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            if (row.get("approve(yes/no)") or "").strip().lower() != "yes":
                continue

            rid = int(row["id"])
            key = (row["from_id"], row["relation"], row["to_id"])
            if key in existing:
                cur.execute("UPDATE staged_relations SET status='applied' WHERE id=?", (rid,))
                continue

            # write canonical row
            with CANON.open("a", newline="", encoding="utf-8") as out:
                w = csv.DictWriter(out, fieldnames=HDR)
                w.writerow({
                    "from_id": row["from_id"],
                    "relation": row["relation"],
                    "to_id": row["to_id"],
                    "source_title": row["source_sha256"],
                    "source_locator": row["locator"],
                    "excerpt": row["excerpt"],
                    "tradition": row.get("tradition","unknown"),
                    "confidence": row.get("confidence","attested_secondary"),
                    "notes": row.get("notes","")
                })
            existing.add(key)
            applied += 1
            cur.execute("UPDATE staged_relations SET status='applied' WHERE id=?", (rid,))

    con.commit()
    con.close()
    print(f"Applied {applied} rows into {CANON}")

def main():
    if "--apply" in sys.argv:
        apply_preview()
    else:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else 50
        export_batch(limit)

if __name__ == "__main__":
    main()
