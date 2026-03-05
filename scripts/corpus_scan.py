import hashlib, sqlite3, time
from pathlib import Path

DB = Path("/opt/atlas/memory/corpus.db")
RESEARCH = Path("/opt/atlas/research")

def sha256_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def kind_of(p: Path) -> str:
    ext = p.suffix.lower()
    if ext == ".pdf": return "pdf"
    if ext in (".txt",".md"): return "txt"
    if ext in (".html",".htm"): return "html"
    if ext in (".zip",".gz",".tgz"): return "zip"
    return "other"

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    seen=0
    added=0
    for p in RESEARCH.rglob("*"):
        if not p.is_file():
            continue
        if "/_text/" in str(p) or "/_meta/" in str(p):
            continue

        seen += 1
        digest = sha256_file(p)
        size = p.stat().st_size
        mtime = int(p.stat().st_mtime)
        kind = kind_of(p)

        cur.execute("SELECT sha256 FROM files WHERE sha256=?", (digest,))
        if cur.fetchone():
            continue

        cur.execute(
            "INSERT INTO files (sha256,path,size,mtime,kind,status,added_ts) VALUES (?,?,?,?,?,?,?)",
            (digest, str(p), size, mtime, kind, "new", int(time.time()))
        )
        added += 1

    con.commit()
    con.close()
    print(f"corpus_scan: seen={seen} new_added={added} db={DB}")

if __name__ == "__main__":
    main()
