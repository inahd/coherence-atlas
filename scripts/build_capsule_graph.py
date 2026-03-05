import csv, json
from pathlib import Path

DATASETS = Path("/opt/atlas/datasets")
OUT = Path("/opt/atlas/memory/vedic_cosmology_graph.json")

TITHI = DATASETS / "tithi_list.csv"
NITYA = DATASETS / "nitya_devi_mapping.csv"
NAKS  = DATASETS / "nakshatra_list.csv"

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def node_id(prefix, raw):
    return f"{prefix}:{str(raw).strip()}"

def main():
    missing = [str(p) for p in (TITHI, NITYA, NAKS) if not p.exists()]
    if missing:
        raise SystemExit(f"Missing required dataset files: {missing}")

    tithis = read_csv(TITHI)
    mappings = read_csv(NITYA)
    nakshatras = read_csv(NAKS)

    nodes, links = [], []
    for r in tithis:
        tid = node_id("tithi", r["id"])
        nodes.append({"id": tid, "type": "Tithi", "name": r.get("name"), "sanskrit": r.get("sanskrit")})

    seen_devi = set()
    for m in mappings:
        tithi_id = node_id("tithi", m["tithi_id"])
        devi_name = m["nitya_devi"].strip()
        devi_id = node_id("nitya_devi", devi_name.lower().replace(" ", "_"))

        if devi_id not in seen_devi:
            nodes.append({"id": devi_id, "type": "NityaDevi", "name": devi_name})
            seen_devi.add(devi_id)

        links.append({
            "source": tithi_id,
            "target": devi_id,
            "relation": "tithi_associated_nitya_devi",
            "evidence": {"dataset": "nitya_devi_mapping.csv"}
        })

    for r in nakshatras:
        nid = node_id("nakshatra", r["id"])
        nodes.append({"id": nid, "type": "Nakshatra", "name": r.get("name")})

    OUT.write_text(json.dumps({"nodes": nodes, "links": links}, indent=2), encoding="utf-8")
    print("Wrote:", OUT)

if __name__ == "__main__":
    main()
