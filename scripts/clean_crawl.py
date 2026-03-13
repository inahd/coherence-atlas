from bs4 import BeautifulSoup
from pathlib import Path

RAW = Path("/opt/atlas/crawl/raw")
CLEAN = Path("/opt/atlas/crawl/clean")

CLEAN.mkdir(exist_ok=True)

for f in RAW.glob("*.html"):

    html = f.read_text(encoding="utf8")
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text()

    out = CLEAN / (f.stem + ".txt")
    out.write_text(text)

    print("cleaned", f.name)
