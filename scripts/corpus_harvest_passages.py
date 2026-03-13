import csv, hashlib, re, sqlite3, time
from pathlib import Path

DB = Path("/opt/atlas/memory/corpus.db")
TEXTDIR = Path("/opt/atlas/research/_text")

DATASETS = Path("/opt/atlas/datasets")

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()[:12]

def load_list(csv_path: Path, col: str):
    if not csv_path.exists():
        return []
    out=[]
    with csv_path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            v=(r.get(col) or "").strip()
            if v: out.append(v)
    return out

def vocab():
    nak = load_list(DATASETS/"nakshatra_list.csv", "name")
    tithi = load_list(DATASETS/"tithi_list.csv", "name")
    return {
        "nakshatra": sorted(set(nak), key=len, reverse=True),
        "tithi": sorted(set(tithi), key=len, reverse=True),
    }

def tag_chunk(text: str, v):
    tags=[]
    for cat, terms in v.items():
        for term in terms[:250]:
            if re.search(rf"\b{re.escape(term)}\b", text, flags=re.I):
                tags.append(f"{cat}:{term}")
    return ";".join(sorted(set(tags)))

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    v = vocab()

    added=0
    for txt in TEXTDIR.glob("*.txt"):
        # find source sha by matching original file stem in files.path
        # fallback: use sha of txt path
        source_sha = hashlib.sha256(str(txt).encode()).hexdigest()

        lines = txt.read_text(encoding="utf-8", errors="ignore").splitlines()
        page=1
        buf=[]
        start=1

        def flush(end):
            nonlocal added, buf, start, page
            chunk="\n".join(buf).strip()
            if not chunk:
                buf=[]
                start=end+1
                return
            tags = tag_chunk(chunk, v)
            if tags:
                pid = "passage:" + sha1(source_sha + ":" + str(page) + ":" + str(start) + ":" + chunk[:200])
                try:
                    cur.execute(
                        "INSERT OR IGNORE INTO passages (passage_id,source_sha256,locator,excerpt,tags,added_ts) VALUES (?,?,?,?,?,?)",
                        (pid, source_sha, f"page {page}, lines {start}-{end}", chunk[:900], tags, int(time.time()))
                    )
                    if cur.rowcount:
                        added += 1
                except Exception:
                    pass
            buf=[]
            start=end+1

        for i,line in enumerate(lines, start=1):
            m=re.match(r"\[page (\d+)\]", line.strip(), re.I)
            if m:
                flush(i-1)
                page=int(m.group(1))
                continue
            buf.append(line)
            if len(buf) >= 24:
                flush(i)
        flush(len(lines))

    con.commit()
    con.close()
    print(f"corpus_harvest_passages: added={added}")

if __name__ == "__main__":
    main()
