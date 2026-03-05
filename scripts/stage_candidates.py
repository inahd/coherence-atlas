import re, sqlite3, sys, time
from pathlib import Path

DB = Path("/opt/atlas/memory/corpus.db")

# very lightweight heuristics for your current graph:
# - if a passage mentions a nakshatra and also mentions a deity-like token near it, stage a candidate.
# You can expand this with curated vocab lists later.

DEITY_HINTS = [
    "brahma","soma","agni","yama","prajapati","vishnu","shiva","indra","varuna","mitra",
    "ashwini","ashvins","kumaras","kumara","surya","chandra"
]

def score_excerpt(excerpt: str, nak_name: str):
    # score by co-occurrence of deity hints; keep simple
    e = excerpt.lower()
    score = 0.0
    for h in DEITY_HINTS:
        if h in e:
            score += 1.0
    if nak_name.lower() in e:
        score += 1.0
    return score

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # pull passages that mention nakshatra tags
    cur.execute("SELECT passage_id, source_sha256, locator, excerpt, tags FROM passages WHERE tags LIKE '%nakshatra:%' LIMIT 2000")
    rows = cur.fetchall()

    staged=0
    for pid, sha, loc, ex, tags in rows:
        # find nakshatra names in tags
        nak_tags = [t for t in (tags or "").split(";") if t.startswith("nakshatra:")]
        for nt in nak_tags:
            nak_name = nt.split(":",1)[1]
            sc = score_excerpt(ex, nak_name)
            if sc < 2.0:
                continue

            # naive deity selection: first deity hint found
            deity = None
            low = ex.lower()
            for h in DEITY_HINTS:
                if h in low:
                    deity = h
                    break
            if not deity:
                continue

            from_id = f"nakshatra:{re.sub(r'[^a-z0-9]+','_', nak_name.lower()).strip('_')}"
            to_id = f"deity:{re.sub(r'[^a-z0-9]+','_', deity.lower()).strip('_')}"
            rel = "nakshatra_associated_deity"

            cur.execute(
                "INSERT INTO staged_relations (from_id,relation,to_id,source_sha256,locator,excerpt,score,status,added_ts) "
                "VALUES (?,?,?,?,?,?,?,?,?)",
                (from_id, rel, to_id, sha, loc, ex[:900], sc, "staged", int(time.time()))
            )
            staged += 1
            if staged >= n:
                con.commit()
                con.close()
                print(f"stage_candidates: staged={staged}")
                return

    con.commit()
    con.close()
    print(f"stage_candidates: staged={staged}")

if __name__ == "__main__":
    main()
