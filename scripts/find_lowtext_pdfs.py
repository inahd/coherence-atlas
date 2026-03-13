from pathlib import Path

RESEARCH = Path("/opt/atlas/research")
TEXTDIR  = RESEARCH / "_text"
OUTLIST  = RESEARCH / "_ocr" / "lowtext_pdfs.txt"
OUTLIST.parent.mkdir(parents=True, exist_ok=True)

def main():
    # match PDFs that have corresponding _text/<stem>.txt with <500 chars
    low = []
    for pdf in RESEARCH.rglob("*.pdf"):
        txt = TEXTDIR / (pdf.stem + ".txt")
        if not txt.exists():
            continue
        try:
            n = len(txt.read_text(encoding="utf-8", errors="ignore").strip())
        except Exception:
            n = 0
        if n < 500:
            low.append(str(pdf))

    OUTLIST.write_text("\n".join(low) + ("\n" if low else ""), encoding="utf-8")
    print(f"lowtext list: {OUTLIST} count={len(low)}")

if __name__ == "__main__":
    main()
