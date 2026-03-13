import sqlite3, json, time
from pathlib import Path

DB = Path("/opt/atlas/memory/corpus.db")
OUT = Path("/opt/atlas/memory/reports/aggregate.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("SELECT kind, COUNT(*) FROM files GROUP BY kind")
    by_kind = dict(cur.fetchall())

    cur.execute("SELECT status, COUNT(*) FROM files GROUP BY status")
    by_status = dict(cur.fetchall())

    cur.execute("SELECT COUNT(*) FROM passages")
    passages = cur.fetchone()[0]

    cur.execute("SELECT tags, COUNT(*) as c FROM passages GROUP BY tags ORDER BY c DESC LIMIT 20")
    top_tags = [{"tags": t, "count": c} for t,c in cur.fetchall()]

    cur.execute("SELECT status, COUNT(*) FROM staged_relations GROUP BY status")
    staged = dict(cur.fetchall())

    con.close()

    OUT.write_text(json.dumps({
        "timestamp": int(time.time()),
        "files_by_kind": by_kind,
        "files_by_status": by_status,
        "passages": passages,
        "top_tags": top_tags,
        "staged_relations": staged
    }, indent=2), encoding="utf-8")
    print("Wrote:", OUT)

if __name__ == "__main__":
    main()
