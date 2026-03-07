import csv, hashlib, sys, time
from pathlib import Path
import urllib.request

OUTDIR = Path("/opt/atlas/research/_incoming_remote")
SOURCES = Path("/opt/atlas/datasets/sources/remote_sources.csv")
OUTDIR.mkdir(parents=True, exist_ok=True)
SOURCES.parent.mkdir(parents=True, exist_ok=True)

HDR = ["fetched_ts","url","local_path","sha256","bytes"]

def sha256_file(p: Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def append_row(row):
    new = not SOURCES.exists()
    with SOURCES.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HDR)
        if new: w.writeheader()
        w.writerow(row)

def main(url: str):
    name = url.split("/")[-1] or "download"
    target = OUTDIR / name
    # avoid overwrite
    if target.exists():
        target = OUTDIR / f"{int(time.time())}_{name}"

    urllib.request.urlretrieve(url, target)
    sz = target.stat().st_size
    dig = sha256_file(target)

    append_row({
        "fetched_ts": int(time.time()),
        "url": url,
        "local_path": str(target),
        "sha256": dig,
        "bytes": sz
    })

    print("saved:", target)
    print("bytes:", sz)
    print("sha256:", dig)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remote_fetch.py <url>")
        raise SystemExit(2)
    main(sys.argv[1])
