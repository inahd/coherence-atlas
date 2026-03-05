import hashlib, json, shutil, time
from pathlib import Path

INCOMING = Path("/opt/atlas/research/_incoming")
RESEARCH  = Path("/opt/atlas/research")
META_DIR  = Path("/opt/atlas/research/_meta")

META_DIR.mkdir(parents=True, exist_ok=True)

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    moved = 0
    skipped = 0
    for f in INCOMING.rglob("*"):
        if not f.is_file():
            continue
        digest = sha256_file(f)
        # keep original filename but ensure uniqueness by digest prefix
        target = RESEARCH / f"{digest[:12]}__{f.name}"
        meta = META_DIR / f"{digest}.json"

        if target.exists():
            skipped += 1
            continue

        shutil.copy2(f, target)
        meta.write_text(json.dumps({
            "sha256": digest,
            "src_path": str(f),
            "dst_path": str(target),
            "timestamp": int(time.time()),
            "size": f.stat().st_size
        }, indent=2), encoding="utf-8")

        moved += 1

    print(f"promote_incoming: moved={moved} skipped_existing={skipped}")

if __name__ == "__main__":
    main()
