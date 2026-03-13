import sqlite3, time
from pathlib import Path
from pypdf import PdfReader

DB = Path("/opt/atlas/memory/corpus.db")
OUTDIR = Path("/opt/atlas/research/_text")
OUTDIR.mkdir(parents=True, exist_ok=True)

def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    parts=[]
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        t = t.strip()
        if t:
            parts.append(f"[page {i+1}]\n{t}")
    return "\n\n".join(parts).strip()

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT sha256,path FROM files WHERE kind='pdf' AND status='new'")
    rows = cur.fetchall()

    ok=0
    low=0
    for sha, path in rows:
        pdf = Path(path)
        out = OUTDIR / (pdf.stem + ".txt")
        try:
            text = extract_pdf_text(pdf)
            out.write_text(text, encoding="utf-8", errors="ignore")
            n=len(text)
            ok += 1
            if n < 500:
                low += 1
                print("[LOW TEXT]", pdf.name, n)
            else:
                print("[OK]", pdf.name, n)

            cur.execute("UPDATE files SET status='extracted' WHERE sha256=?", (sha,))
            con.commit()
        except Exception as e:
            print("[FAIL]", pdf.name, e)

    con.close()
    print(f"corpus_extract_pdftext: processed={ok} low_text={low}")

if __name__ == "__main__":
    main()
