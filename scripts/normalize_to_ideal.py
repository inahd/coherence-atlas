import csv, re
from pathlib import Path
import yaml

BASE = Path("/opt/atlas")
DS = BASE / "datasets"
ENT = DS / "entities"
REL = DS / "relations"
SEED = DS / "seed"

ENT.mkdir(parents=True, exist_ok=True)
REL.mkdir(parents=True, exist_ok=True)
SEED.mkdir(parents=True, exist_ok=True)

def slugify(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "unknown"

def write_entities(outfile: Path, rows):
    hdr = ["id","type","name","aliases","notes","source_file"]
    with outfile.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=hdr)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k,"") for k in hdr})

def read_yaml(path: Path):
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text(encoding="utf-8", errors="ignore"))

def extract_entities(obj, etype: str, source_file: str):
    rows = []
    if obj is None:
        return rows

    # Common YAML shapes:
    # - list of strings
    # - list of dicts with name/id/aliases
    # - dict of key->dict or key->string
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, str):
                name = item
                rows.append({
                    "id": f"{etype}:{slugify(name)}",
                    "type": etype,
                    "name": name,
                    "aliases": "",
                    "notes": "",
                    "source_file": source_file
                })
            elif isinstance(item, dict):
                name = item.get("name") or item.get("title") or item.get("id") or ""
                aliases = item.get("aliases") or item.get("alias") or ""
                if isinstance(aliases, list):
                    aliases = ";".join([str(a) for a in aliases])
                rid = item.get("id")
                rid = f"{etype}:{slugify(rid or name)}"
                rows.append({
                    "id": rid,
                    "type": etype,
                    "name": name or rid.split(":",1)[1],
                    "aliases": aliases,
                    "notes": item.get("notes","") or "",
                    "source_file": source_file
                })
    elif isinstance(obj, dict):
        for k,v in obj.items():
            if isinstance(v, str):
                name = v or k
                rows.append({
                    "id": f"{etype}:{slugify(k)}",
                    "type": etype,
                    "name": name,
                    "aliases": "",
                    "notes": "",
                    "source_file": source_file
                })
            elif isinstance(v, dict):
                name = v.get("name") or v.get("title") or k
                aliases = v.get("aliases") or ""
                if isinstance(aliases, list):
                    aliases = ";".join([str(a) for a in aliases])
                rid = v.get("id")
                rid = f"{etype}:{slugify(rid or k)}"
                rows.append({
                    "id": rid,
                    "type": etype,
                    "name": name,
                    "aliases": aliases,
                    "notes": v.get("notes","") or "",
                    "source_file": source_file
                })
            else:
                # fallback: treat key as name
                rows.append({
                    "id": f"{etype}:{slugify(k)}",
                    "type": etype,
                    "name": str(k),
                    "aliases": "",
                    "notes": "",
                    "source_file": source_file
                })
    return rows

def main():
    mappings = [
        ("deities.yaml", "deity"),
        ("graha.yaml", "graha"),
        ("nakshatra.yaml", "nakshatra"),
        ("vedic_concepts.yaml", "concept"),
        ("texts.yaml", "text"),
        ("jyotish_core.yaml", "jyotish"),
        ("rashi.yaml", "rashi"),
    ]

    for fname, etype in mappings:
        src = DS / fname
        obj = read_yaml(src)
        rows = extract_entities(obj, etype, fname)
        if rows:
            out = ENT / f"{etype}.csv"
            write_entities(out, rows)
            print(f"[OK] entities → {out} ({len(rows)} rows)")
        else:
            print(f"[SKIP] {fname} missing/empty or not parseable")

    # Move existing unfilled relations into seed/
    for f in DS.glob("relations_*.csv"):
        dest = SEED / f.name
        if dest.exists():
            continue
        dest.write_text(f.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")
        print(f"[OK] moved to seed → {dest}")

    print("\nNormalization complete.\n")

if __name__ == "__main__":
    main()
