import requests
from pathlib import Path

SOURCES = [
    "https://en.wikipedia.org/wiki/Vedic_cosmology",
    "https://en.wikipedia.org/wiki/Jyotisha",
]

RAW = Path("/opt/atlas/crawl/raw")
RAW.mkdir(parents=True, exist_ok=True)

for url in SOURCES:
    try:
        r = requests.get(url, timeout=20)
        name = url.split("/")[-1] + ".html"
        with open(RAW / name, "w", encoding="utf8") as f:
            f.write(r.text)

        print("saved", url)

    except Exception as e:
        print("error", url, e)
