import csv, os, re, sqlite3
from pathlib import Path

BASE = Path("/opt/atlas")
DS = BASE/"datasets"
PASSAGES_CSV = DS/"sources"/"passages.csv"
CORPUS_DB = BASE/"memory"/"corpus.db"

REL_FILES = [
    DS/"relations_nakshatra_deity.csv",
    DS/"relations_devi_weapon.csv",
    DS/"relations_nakshatra_plants.csv",
    DS/"relations_ritual_calendar.csv",
    DS/"relations_raga_ritual.csv",
    DS/"relations_nakshatra_graha.csv",
]

HDR = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"]
EVID = ["source_title","source_locator","excerpt"]

def read_csv(p: Path):
    if not p.exists(): return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(p: Path, rows):
    # preserve required header order
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HDR)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k,"") for k in HDR})

def clean(x: str) -> str:
    x=(x or "").strip()
    if ":" in x: x=x.split(":",1)[1]
    return x.replace("_"," ").lower()

def ev_missing(r):
    return not all((r.get(k) or "").strip() for k in EVID)

def load_passages_csv():
    if not PASSAGES_CSV.exists(): return []
    with PASSAGES_CSV.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_passages_db(limit=50000):
    if not CORPUS_DB.exists(): return []
    con = sqlite3.connect(CORPUS_DB)
    cur = con.cursor()
    cur.execute("SELECT source_sha256, locator, excerpt, tags FROM passages LIMIT ?", (limit,))
    rows = [{"source_id": r[0], "locator": r[1], "excerpt": r[2], "tags": r[3]} for r in cur.fetchall()]
    con.close()
    return rows

def tag_match(passages, need_any):
    # need_any: list of strings; return first passage whose tags contain any
    for p in passages:
        tags = (p.get("tags") or "")
        for t in need_any:
            if t and t in tags:
                return p
    return None

def text_match(passages, a, b):
    for p in passages:
        txt=(p.get("excerpt") or "").lower()
        if a in txt and b in txt:
            return p
    return None

def infer_tag_variants(_id: str):
    # tags look like "nakshatra:Rohini" in some pipelines; try a few variants
    if ":" not in _id:
        return []
    typ, val = _id.split(":",1)
    val2 = val.replace("_"," ")
    return [
        f"{typ}:{val}",
        f"{typ}:{val2}",
        f"{typ}:{val2.title()}",
        f"{typ}:{val.replace('_','')}",
    ]

def main():
    N = int(os.environ.get("N_EVID", "250"))
    upgraded = 0

    passages = load_passages_db() + load_passages_csv()

    for relf in REL_FILES:
        if upgraded >= N:
            break
        if not relf.exists():
            continue
        rows = read_csv(relf)
        changed = False

        for r in rows:
            if upgraded >= N:
                break
            if not (r.get("to_id") or "").strip():
                continue
            if not ev_missing(r):
                continue

            a = clean(r.get("from_id",""))
            b = clean(r.get("to_id",""))

            # first try tag-based match
            need = infer_tag_variants(r.get("from_id","")) + infer_tag_variants(r.get("to_id",""))
            hit = tag_match(passages, need) if need else None

            # fallback: co-mention in excerpt
            if not hit:
                hit = text_match(passages, a, b)

            if not hit:
                continue

            r["source_title"] = (r.get("source_title") or "").strip() or (hit.get("source_id") or "unknown")
            r["source_locator"] = (r.get("source_locator") or "").strip() or (hit.get("locator") or "unknown")
            r["excerpt"] = (r.get("excerpt") or "").strip() or (hit.get("excerpt") or "")[:900]
            r["tradition"] = (r.get("tradition") or "unknown").strip() or "unknown"

            conf = (r.get("confidence") or "").strip()
            if conf in ("", "seed_unverified", "auto_proposed"):
                r["confidence"] = "attested_secondary"

            note = (r.get("notes") or "")
            if "EVID2" not in note:
                r["notes"] = (note + " | EVID2: tag/text match").strip(" |")

            upgraded += 1
            changed = True

        if changed:
            write_csv(relf, rows)

    print("evidencefill_v2 upgraded:", upgraded)

if __name__ == "__main__":
    main()
