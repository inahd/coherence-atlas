import csv, re, sys
from pathlib import Path

RESEARCH = Path("/opt/atlas/research")
DATASETS = Path("/opt/atlas/datasets")

REL_FILES = [
    DATASETS / "relations_nakshatra_deity.csv",
    DATASETS / "relations_devi_weapon.csv",
    DATASETS / "relations_nakshatra_plants.csv",
    DATASETS / "relations_ritual_calendar.csv",
    DATASETS / "relations_raga_ritual.csv",
]

HDR = ["from_id","relation","to_id","source_title","source_locator","excerpt","tradition","confidence","notes"]

def clean_term(x: str) -> str:
    # turn deity:ashwini_kumaras -> ashwini kumaras
    x = (x or "").strip()
    if ":" in x:
        x = x.split(":",1)[1]
    return x.replace("_"," ").strip()

def find_evidence(term_a: str, term_b: str, max_chars=260):
    """
    Search text files for lines where both terms appear within a small window.
    Returns (source_title, source_locator, excerpt) or None.
    """
    if not RESEARCH.exists():
        return None

    a = term_a.lower()
    b = term_b.lower()

    for p in RESEARCH.rglob("*"):
        if not p.is_file():
            continue
        # skip huge binaries by extension
        if p.suffix.lower() in {".png",".jpg",".jpeg",".webp",".gif",".zip",".pdf"}:
            continue

        try:
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue

        # quick pass: find lines containing a or b
        for i, line in enumerate(lines):
            L = line.lower()
            if a in L or b in L:
                # look +/- 6 lines for the other term
                lo = max(0, i-6)
                hi = min(len(lines), i+7)
                window = "\n".join(lines[lo:hi])
                W = window.lower()
                if a in W and b in W:
                    excerpt = window.strip()
                    if len(excerpt) > max_chars:
                        excerpt = excerpt[:max_chars].rstrip() + "…"
                    locator = f"lines {lo+1}-{hi}"
                    return (p.name, locator, excerpt)

    return None

def load_rows(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_rows(path: Path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HDR)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k,"") for k in HDR})

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    updated = 0
    scanned = 0

    for relfile in REL_FILES:
        if updated >= n:
            break
        if not relfile.exists():
            continue

        rows = load_rows(relfile)
        changed = False

        for r in rows:
            if updated >= n:
                break

            scanned += 1

            # Only propose evidence if to_id exists and evidence is missing
            if not (r.get("to_id") or "").strip():
                continue
            ev_ok = all((r.get(k) or "").strip() for k in ["source_title","source_locator","excerpt"])
            if ev_ok:
                continue

            from_term = clean_term(r.get("from_id",""))
            to_term   = clean_term(r.get("to_id",""))

            hit = find_evidence(from_term, to_term)
            if not hit:
                continue

            source_title, locator, excerpt = hit

            r["source_title"] = r.get("source_title") or source_title
            r["source_locator"] = r.get("source_locator") or locator
            r["excerpt"] = r.get("excerpt") or excerpt
            r["tradition"] = (r.get("tradition") or "").strip() or "unknown"
            # maturity step: only upgrade when we found evidence
            if (r.get("confidence") or "").strip() in ("", "seed_unverified"):
                r["confidence"] = "attested_secondary"
            note = (r.get("notes") or "")
            if "EVID" not in note:
                r["notes"] = (note + " | EVID: auto-found in research corpus").strip(" |")

            updated += 1
            changed = True

        if changed:
            write_rows(relfile, rows)

    print(f"Propose evidence complete. Updated {updated} rows (scanned {scanned}).")
    print("Next: atlas factcheck (missing evidence should drop), atlas seedgraph, atlas graph seed.")

if __name__ == "__main__":
    main()
