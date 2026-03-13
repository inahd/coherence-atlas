import re, csv, hashlib, sys, json
from pathlib import Path
from pypdf import PdfReader

BASE = Path("/opt/atlas")
DATASETS = BASE / "datasets"
SOURCES = DATASETS / "sources"
TEXTDIR = BASE / "research" / "_text"

SOURCES_CSV = SOURCES / "sources.csv"
PASSAGES_CSV = SOURCES / "passages.csv"

def ensure_csv(path: Path, header):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(header)

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()[:12]

def file_id(p: Path) -> str:
    # stable ID so _text outputs won't collide for same stem in different dirs
    return hashlib.sha1(str(p.resolve()).encode("utf-8", errors="ignore")).hexdigest()[:8]

def load_list_csv(path: Path, col="name"):
    if not path.exists():
        return []
    out=[]
    with path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            v=(r.get(col) or "").strip()
            if v: out.append(v)
    return out

def build_vocab():
    nak = load_list_csv(DATASETS/"nakshatra_list.csv", "name")
    tithi = load_list_csv(DATASETS/"tithi_list.csv", "name")
    if not nak:
        nak = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha",
               "Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula",
               "Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]
    if not tithi:
        tithi = ["Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dashami",
                 "Ekadashi","Dwadashi","Trayodashi","Chaturdashi","Purnima","Amavasya"]
    return {
        "nakshatra": sorted(set(nak), key=len, reverse=True),
        "tithi": sorted(set(tithi), key=len, reverse=True),
    }

def extract_pdf_text(pdf_path: Path) -> Path:
    TEXTDIR.mkdir(parents=True, exist_ok=True)
    out = TEXTDIR / f"{pdf_path.stem}__{file_id(pdf_path)}.txt"

    reader = PdfReader(str(pdf_path))
    parts=[]
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        t = t.strip()
        if t:
            parts.append(f"[page {i+1}]\n{t}")
    out.write_text("\n\n".join(parts), encoding="utf-8", errors="ignore")
    return out

def harvest_passages(txt_path: Path, source_id: str, vocab: dict):
    lines = txt_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    patterns = {}
    for k, terms in vocab.items():
        patterns[k] = [(term, re.compile(rf"\b{re.escape(term)}\b", re.I)) for term in terms]

    passages=[]
    current_page = 1
    buf=[]
    buf_start = 1

    def flush(buf, start_line, end_line, page):
        if not buf:
            return
        text = "\n".join(buf).strip()
        if not text:
            return

        tags=[]
        for cat, plist in patterns.items():
            for term, rx in plist:
                if rx.search(text):
                    tags.append(f"{cat}:{term}")

        if tags:
            pid = f"passage:{sha1(source_id + ':' + str(page) + ':' + str(start_line) + ':' + text[:200])}"
            passages.append({
                "passage_id": pid,
                "source_id": source_id,
                "locator": f"page {page}, lines {start_line}-{end_line}",
                "excerpt": text[:900],
                "tags": ";".join(sorted(set(tags)))
            })

    for idx, line in enumerate(lines, start=1):
        m = re.match(r"\[page (\d+)\]", line.strip(), re.I)
        if m:
            flush(buf, buf_start, idx-1, current_page)
            current_page = int(m.group(1))
            buf=[]
            buf_start = idx+1
            continue

        buf.append(line)
        if len(buf) >= 20:
            flush(buf, buf_start, idx, current_page)
            buf=[]
            buf_start = idx+1

    flush(buf, buf_start, len(lines), current_page)
    return passages

def upsert_source(source_path: Path, title: str):
    ensure_csv(SOURCES_CSV, ["source_id","title","path","notes"])
    sid = f"source:{sha1(str(source_path.resolve()))}"
    existing=set()
    with SOURCES_CSV.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            existing.add(r["source_id"])
    if sid not in existing:
        with SOURCES_CSV.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([sid, title, str(source_path), ""])
    return sid

def write_passages(rows):
    ensure_csv(PASSAGES_CSV, ["passage_id","source_id","locator","excerpt","tags"])
    existing=set()
    with PASSAGES_CSV.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            existing.add(r["passage_id"])

    added=0
    with PASSAGES_CSV.open("a", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=["passage_id","source_id","locator","excerpt","tags"])
        for r in rows:
            if r["passage_id"] in existing:
                continue
            w.writerow(r)
            added += 1
    return added

def main():
    if len(sys.argv) < 2:
        print("Usage: atlas harvestpdf /path/to/file.pdf")
        sys.exit(1)

    pdf_arg = " ".join(sys.argv[1:]).strip()
    pdf_path = Path(pdf_arg).expanduser()
    if not pdf_path.exists():
        print("Missing PDF:", pdf_path)
        sys.exit(1)

    vocab = build_vocab()
    txt_path = extract_pdf_text(pdf_path)
    sid = upsert_source(pdf_path, pdf_path.stem)

    passages = harvest_passages(txt_path, sid, vocab)
    added = write_passages(passages)

    text = txt_path.read_text(encoding="utf-8", errors="ignore").strip()
    chars = len(text)

    # JSON line for machine parsing
    print(json.dumps({
        "ok": True,
        "pdf": str(pdf_path),
        "text": str(txt_path),
        "text_chars": chars,
        "source_id": sid,
        "passages_found": len(passages),
        "passages_added": added
    }))

if __name__ == "__main__":
    main()
