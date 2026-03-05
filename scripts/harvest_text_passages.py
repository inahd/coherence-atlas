import csv, hashlib, re
from pathlib import Path

DATASETS = Path("/opt/atlas/datasets")
SOURCES  = DATASETS / "sources"
PASSAGES = SOURCES / "passages.csv"
SOURCES_CSV = SOURCES / "sources.csv"

TEXTDIR = Path("/opt/atlas/research/_text")

SOURCES.mkdir(parents=True, exist_ok=True)

def ensure_csv(path: Path, header):
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(header)

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()[:12]

def load_vocab():
    # minimal vocab from your existing csvs
    def load_list(csv_path, col):
        out=[]
        if not csv_path.exists():
            return out
        with csv_path.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                v=(r.get(col) or "").strip()
                if v: out.append(v)
        return out

    nak = load_list(DATASETS/"nakshatra_list.csv", "name")
    tithi = load_list(DATASETS/"tithi_list.csv", "name")
    return {
        "nakshatra": sorted(set(nak), key=len, reverse=True),
        "tithi": sorted(set(tithi), key=len, reverse=True),
    }

def tag_chunk(text: str, vocab):
    tags=[]
    for cat, terms in vocab.items():
        for term in terms[:200]:
            if re.search(rf"\b{re.escape(term)}\b", text, flags=re.I):
                tags.append(f"{cat}:{term}")
    return ";".join(sorted(set(tags)))

def upsert_source(title: str, path: str):
    ensure_csv(SOURCES_CSV, ["source_id","title","path","notes"])
    sid = f"source:{sha1(path)}"
    existing=set()
    with SOURCES_CSV.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            existing.add(r["source_id"])
    if sid not in existing:
        with SOURCES_CSV.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([sid, title, path, ""])
    return sid

def main():
    ensure_csv(PASSAGES, ["passage_id","source_id","locator","excerpt","tags"])
    existing=set()
    with PASSAGES.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            existing.add(r["passage_id"])

    vocab = load_vocab()
    added=0

    for txt in TEXTDIR.glob("*.txt"):
        sid = upsert_source(txt.stem, str(txt))
        lines = txt.read_text(encoding="utf-8", errors="ignore").splitlines()

        page = 1
        buf=[]
        start_line=1

        def flush(end_line):
            nonlocal added, buf, start_line
            chunk="\n".join(buf).strip()
            if not chunk:
                buf=[]
                start_line=end_line+1
                return
            tags = tag_chunk(chunk, vocab)
            if tags:
                pid = f"passage:{sha1(sid + ':' + str(page) + ':' + str(start_line) + ':' + chunk[:200])}"
                if pid not in existing:
                    with PASSAGES.open("a", newline="", encoding="utf-8") as f:
                        w=csv.DictWriter(f, fieldnames=["passage_id","source_id","locator","excerpt","tags"])
                        w.writerow({
                            "passage_id": pid,
                            "source_id": sid,
                            "locator": f"page {page}, lines {start_line}-{end_line}",
                            "excerpt": chunk[:900],
                            "tags": tags
                        })
                    existing.add(pid)
                    added += 1
            buf=[]
            start_line=end_line+1

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

    print(f"harvest_text_passages: added={added} passages into {PASSAGES}")

if __name__ == "__main__":
    main()
