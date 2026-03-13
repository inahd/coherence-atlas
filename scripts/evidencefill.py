import csv, sys, re
from pathlib import Path

DATASETS = Path("/opt/atlas/datasets")
PASSAGES = DATASETS / "sources" / "passages.csv"

REL_FILES = [
    DATASETS / "relations_nakshatra_deity.csv",
    DATASETS / "relations_devi_weapon.csv",
    DATASETS / "relations_nakshatra_plants.csv",
    DATASETS / "relations_ritual_calendar.csv",
    DATASETS / "relations_raga_ritual.csv",
]

HDR = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"]

def clean_term(x: str) -> str:
    x=(x or "").strip()
    if ":" in x: x=x.split(":",1)[1]
    return x.replace("_"," ").lower()

def load_passages():
    if not PASSAGES.exists():
        return []
    with PASSAGES.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_rows(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_rows(path: Path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=HDR)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k,"") for k in HDR})

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    passages = load_passages()

    updated=0
    for rel in REL_FILES:
        if updated >= n:
            break
        rows = load_rows(rel)
        changed=False
        for r in rows:
            if updated >= n:
                break
            if not (r.get("to_id") or "").strip():
                continue
            ev_ok = all((r.get(k) or "").strip() for k in ["source_title","source_locator","excerpt"])
            if ev_ok:
                continue

            a = clean_term(r.get("from_id",""))
            b = clean_term(r.get("to_id",""))
            if not a or not b:
                continue

            best=None
            for p in passages:
                text=(p.get("excerpt") or "").lower()
                if a in text and b in text:
                    best=p
                    break

            if not best:
                continue

            r["source_title"] = r.get("source_title") or best.get("source_id","")
            r["source_locator"] = r.get("source_locator") or best.get("locator","")
            r["excerpt"] = r.get("excerpt") or best.get("excerpt","")
            if (r.get("confidence") or "").strip() in ("", "seed_unverified"):
                r["confidence"] = "attested_secondary"
            r["tradition"] = (r.get("tradition") or "unknown").strip() or "unknown"
            note=(r.get("notes") or "")
            if "EVID" not in note:
                r["notes"] = (note + " | EVID: passages.csv").strip(" |")
            updated += 1
            changed=True

        if changed:
            write_rows(rel, rows)

    print(f"evidencefill updated={updated} rows (target={n})")

if __name__ == "__main__":
    main()
