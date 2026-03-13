import csv, json
from pathlib import Path
from collections import Counter

BASE = Path("/opt/atlas")
SCHEMA = BASE / "schemas" / "atlas_projection.json"
DATASETS = BASE / "datasets"
MEMORY = BASE / "memory"

def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    if not SCHEMA.exists():
        raise SystemExit(f"Missing schema: {SCHEMA}")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    expected = schema.get("canonical_datasets_expected", [])
    expected_rel = schema.get("relation_datasets_expected", [])

    print("\nProjection validation\n")

    missing = [f for f in expected if not (DATASETS / f).exists()]
    missing_rel = [f for f in expected_rel if not (DATASETS / f).exists()]

    if missing:
        print("[WARN] Missing canonical datasets:")
        for f in missing: print("  -", f)
    else:
        print("[OK] Canonical datasets present:", ", ".join(expected))

    if missing_rel:
        print("[INFO] Relation datasets not yet present (these unlock more domains):")
        for f in missing_rel: print("  -", f)
    else:
        print("[OK] Relation datasets present:", ", ".join(expected_rel))

    # core counts from capsule datasets
    tithis = read_csv(DATASETS / "tithi_list.csv")
    naks = read_csv(DATASETS / "nakshatra_list.csv")
    nitya_map = read_csv(DATASETS / "nitya_devi_mapping.csv")

    uniq_nitya = len({(r.get("nitya_devi") or "").strip() for r in nitya_map if (r.get("nitya_devi") or "").strip()})

    print("\nCore coverage (current):")
    print("  tithis:", len(tithis))
    print("  nakshatras:", len(naks))
    print("  nitya_devis (unique):", uniq_nitya)
    print("  tithi→nitya mapping rows:", len(nitya_map))

    # evidence coverage if capsule graph exists
    cap = MEMORY / "vedic_cosmology_graph.json"
    if cap.exists():
        g = json.loads(cap.read_text(encoding="utf-8"))
        links = g.get("links", [])
        total = len(links)
        with_ev = sum(1 for e in links if isinstance(e, dict) and e.get("evidence"))
        print("\nEvidence on canonical links:")
        print(f"  links with evidence: {with_ev}/{total}")
    else:
        print("\n[INFO] No vedic_cosmology_graph.json found yet (run: atlas capsule_build)")

    print("\nDone.\n")

if __name__ == "__main__":
    main()
