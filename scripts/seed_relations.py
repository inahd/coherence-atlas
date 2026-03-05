import csv
from pathlib import Path

DATASETS = Path("/opt/atlas/datasets")

HDR = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"]

def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def append_rows(path: Path, rows):
    # prevent duplicates by (from_id, relation)
    existing = set()
    with path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            existing.add((r.get("from_id",""), r.get("relation","")))

    added = 0
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HDR)
        for r in rows:
            key = (r["from_id"], r["relation"])
            if key not in existing:
                w.writerow(r)
                added += 1
    return added

def main():
    tithi_list = read_csv(DATASETS / "tithi_list.csv")
    nak_list   = read_csv(DATASETS / "nakshatra_list.csv")
    nitya_map  = read_csv(DATASETS / "nitya_devi_mapping.csv")

    if not nak_list:
        print("[WARN] nakshatra_list.csv missing or empty — cannot seed nakshatra relations.")
    if not nitya_map:
        print("[WARN] nitya_devi_mapping.csv missing or empty — cannot seed devi_weapon stubs.")

    # Unique nitya devi names
    nitya_devis = sorted({(r.get("nitya_devi") or "").strip() for r in nitya_map if (r.get("nitya_devi") or "").strip()})

    # A) Nakshatra→Deity (27 stubs)
    rows = []
    for r in nak_list:
        nid = f"nakshatra:{r['id'].strip()}"
        rows.append({
            "from_id": nid,
            "relation": "nakshatra_associated_deity",
            "to_id": "",
            "source_title": "",
            "source_locator": "",
            "excerpt": "",
            "tradition": "",
            "confidence": "seed_unverified",
            "notes": "TODO: fill deity + evidence"
        })
    added_a = append_rows(DATASETS / "relations_nakshatra_deity.csv", rows)

    # B) Devi→Weapon (stubs from NityaDevi list)
    rows = []
    for name in nitya_devis:
        did = "devi:" + name.lower().replace(" ", "_")
        rows.append({
            "from_id": did,
            "relation": "devi_wields_weapon",
            "to_id": "",
            "source_title": "",
            "source_locator": "",
            "excerpt": "",
            "tradition": "",
            "confidence": "seed_unverified",
            "notes": "TODO: fill weapon + evidence"
        })
    added_b = append_rows(DATASETS / "relations_devi_weapon.csv", rows)

    # C) Nakshatra→Plant (27 stubs)
    rows = []
    for r in nak_list:
        nid = f"nakshatra:{r['id'].strip()}"
        rows.append({
            "from_id": nid,
            "relation": "nakshatra_sacred_plant",
            "to_id": "",
            "source_title": "",
            "source_locator": "",
            "excerpt": "",
            "tradition": "",
            "confidence": "seed_unverified",
            "notes": "TODO: fill plant + evidence"
        })
    added_c = append_rows(DATASETS / "relations_nakshatra_plants.csv", rows)

    print("\nSeed summary:")
    print("  relations_nakshatra_deity added:", added_a)
    print("  relations_devi_weapon     added:", added_b)
    print("  relations_nakshatra_plants added:", added_c)
    print("\nFiles live in: /opt/atlas/datasets/\n")

if __name__ == "__main__":
    main()
