import csv, re
from pathlib import Path
import yaml

DS = Path("/opt/atlas/datasets")

REL_NAK_DEITY = DS / "relations_nakshatra_deity.csv"
REL_NAK_GRAHA = DS / "relations_nakshatra_graha.csv"
NAK_LIST_CSV  = DS / "nakshatra_list.csv"
NAK_YAML      = DS / "nakshatra.yaml"

HDR = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"]

def slugify(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "unknown"

def normalize_key(name: str) -> str:
    # your YAML keys are like "PurvaPhalguni" (no spaces)
    return re.sub(r"[^A-Za-z0-9]", "", name or "")

def read_csv(path: Path):
    if not path.exists(): return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HDR)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k,"") for k in HDR})

def ensure_csv(path: Path):
    if not path.exists():
        write_csv(path, [])

def load_yaml(path: Path):
    if not path.exists(): return None
    return yaml.safe_load(path.read_text(encoding="utf-8", errors="ignore"))

def main():
    for p in [REL_NAK_DEITY, NAK_LIST_CSV, NAK_YAML]:
        if not p.exists():
            print("Missing:", p)
            return

    # id -> display name from nakshatra_list.csv
    id_to_name = {}
    for r in read_csv(NAK_LIST_CSV):
        _id = (r.get("id") or "").strip()
        nm  = (r.get("name") or "").strip()
        if _id and nm:
            id_to_name[_id] = nm

    ny = load_yaml(NAK_YAML)
    if not isinstance(ny, dict):
        print("nakshatra.yaml not a dict keyed by name; cannot autolink.")
        return

    # nameKey -> (deity, ruler)
    name_to_deity = {}
    name_to_ruler = {}
    for k, v in ny.items():
        if not isinstance(v, dict):
            continue
        kk = normalize_key(k)
        if v.get("deity"):
            name_to_deity[kk] = str(v["deity"]).strip()
        if v.get("ruler"):
            name_to_ruler[kk] = str(v["ruler"]).strip()

    # ---- Fill nakshatra→deity ----
    rows = read_csv(REL_NAK_DEITY)
    changed_deity = 0
    for r in rows:
        if (r.get("relation") or "").strip() != "nakshatra_associated_deity":
            continue
        if (r.get("to_id") or "").strip():
            continue
        src = (r.get("from_id") or "").strip()  # nakshatra:04 etc
        if not src.startswith("nakshatra:"):
            continue
        raw_id = src.split(":", 1)[1]
        nm = id_to_name.get(raw_id)
        if not nm:
            continue
        deity = name_to_deity.get(normalize_key(nm))
        if not deity:
            continue
        r["to_id"] = f"deity:{slugify(deity)}"
        r["confidence"] = (r.get("confidence") or "seed_unverified") or "seed_unverified"
        note = (r.get("notes") or "")
        if "AUTO" not in note:
            r["notes"] = (note + " | AUTO: deity from nakshatra.yaml").strip(" |")
        changed_deity += 1
    write_csv(REL_NAK_DEITY, rows)

    # ---- Create/fill nakshatra→graha ruler ----
    ensure_csv(REL_NAK_GRAHA)
    existing = {(r.get("from_id",""), r.get("relation","")) for r in read_csv(REL_NAK_GRAHA)}
    graha_rows = read_csv(REL_NAK_GRAHA)
    changed_graha = 0

    for _id, nm in id_to_name.items():
        src = f"nakshatra:{_id}"
        rel = "nakshatra_ruling_graha"
        if (src, rel) in existing:
            continue
        ruler = name_to_ruler.get(normalize_key(nm))
        if not ruler:
            continue
        graha_rows.append({
            "from_id": src,
            "relation": rel,
            "to_id": f"graha:{slugify(ruler)}",
            "source_title": "",
            "source_locator": "",
            "excerpt": "",
            "tradition": "",
            "confidence": "seed_unverified",
            "notes": "AUTO: ruler from nakshatra.yaml"
        })
        changed_graha += 1

    write_csv(REL_NAK_GRAHA, graha_rows)

    print("\nAutolink results:")
    print(f"  nakshatra→deity filled: {changed_deity}/27 (where blank)")
    print(f"  nakshatra→graha added:  {changed_graha} rows into relations_nakshatra_graha.csv")
    print("\nNext: atlas factcheck (evidence still missing, expected)\n")

if __name__ == "__main__":
    main()
