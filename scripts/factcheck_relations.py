import csv
from pathlib import Path

DATASETS = Path("/opt/atlas/datasets")

REL_FILES = [
    "relations_nakshatra_deity.csv",
    "relations_devi_weapon.csv",
    "relations_nakshatra_plants.csv",
    "relations_ritual_calendar.csv",
    "relations_raga_ritual.csv"
]

REQUIRED = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence"]

def main():
    print("\nAtlas Factcheck (canonical hygiene)\n")
    total = 0
    missing_to = 0
    missing_evidence = 0

    for f in REL_FILES:
        path = DATASETS / f
        if not path.exists():
            print(f"[MISSING FILE] {f}")
            continue

        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
        print(f"{f}: {len(rows)} rows")
        for r in rows:
            total += 1
            if not (r.get("to_id") or "").strip():
                missing_to += 1
            # evidence = source_title + locator + excerpt (minimal)
            ev_ok = all((r.get(k) or "").strip() for k in ["source_title","source_locator","excerpt"])
            if not ev_ok:
                missing_evidence += 1

    print("\nSummary:")
    print("  total rows:", total)
    print("  rows missing to_id:", missing_to)
    print("  rows missing evidence:", missing_evidence)
    print("\nTip:")
    print("  Fill to_id + evidence, then change confidence to: attested_secondary or canonical.\n")

if __name__ == "__main__":
    main()
