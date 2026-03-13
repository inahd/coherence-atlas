from pathlib import Path
from pypdf import PdfReader

RESEARCH = Path("/opt/atlas/research")
OUTDIR = RESEARCH / "_text"
OUTDIR.mkdir(parents=True, exist_ok=True)

def extract_one(pdf: Path, out_txt: Path) -> tuple[bool, int]:
    try:
        reader = PdfReader(str(pdf))
        parts = []
        for i, page in enumerate(reader.pages):
            t = page.extract_text() or ""
            t = t.strip()
            if t:
                parts.append(f"[page {i+1}]\n{t}")
        text = "\n\n".join(parts).strip()
        out_txt.write_text(text, encoding="utf-8", errors="ignore")
        return True, len(text)
    except Exception:
        return False, 0

def main():
    ok = low = fail = 0
    for pdf in RESEARCH.rglob("*.pdf"):
        out = OUTDIR / (pdf.stem + ".txt")
        success, n = extract_one(pdf, out)
        if not success:
            fail += 1
            print("[FAIL]", pdf.name)
        else:
            ok += 1
            if n < 500:
                low += 1
                print("[LOW TEXT]", pdf.name, n)
            else:
                print("[OK]", pdf.name, n)
    print(f"pdftext_all done. ok={ok} low_text={low} fail={fail} outdir={OUTDIR}")

if __name__ == "__main__":
    main()
