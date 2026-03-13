from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from pypdf import PdfReader

RESEARCH = Path("/opt/atlas/research")
OUTDIR = RESEARCH / "_text"
OUTDIR.mkdir(parents=True, exist_ok=True)

def extract_one(pdf_path: str):
    pdf = Path(pdf_path)
    out = OUTDIR / (pdf.stem + ".txt")
    reader = PdfReader(str(pdf))
    parts=[]
    for i, page in enumerate(reader.pages):
        t = (page.extract_text() or "").strip()
        if t:
            parts.append(f"[page {i+1}]\n{t}")
    text="\n\n".join(parts).strip()
    out.write_text(text, encoding="utf-8", errors="ignore")
    return pdf.name, len(text)

def main():
    pdfs=[str(p) for p in RESEARCH.rglob("*.pdf")]
    if not pdfs:
        print("no pdfs"); return
    workers=4
    ok=0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs=[ex.submit(extract_one,p) for p in pdfs]
        for f in as_completed(futs):
            name,n=f.result()
            ok+=1
            print("[OK]", name, n)
    print("done", ok)

if __name__=="__main__":
    main()
