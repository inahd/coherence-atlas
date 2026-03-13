import csv, json
from pathlib import Path

BASE = Path("/opt/atlas")
ENT = BASE / "datasets" / "entities"
REL = BASE / "datasets" / "relations"
OUT = BASE / "memory" / "graphs" / "canonical_graph.json"

EVIDENCE_FIELDS = ["source_title","source_locator","excerpt","tradition","confidence"]

def read_csv(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    nodes = {}
    links = []

    # load entities/*.csv
    for p in ENT.glob("*.csv"):
        for r in read_csv(p):
            _id = (r.get("id") or "").strip()
            if not _id:
                continue
            nodes[_id] = {
                "id": _id,
                "type": (r.get("type") or p.stem),
                "name": r.get("name",""),
                "aliases": r.get("aliases",""),
                "notes": r.get("notes","")
            }

    # load canonical relations/*.csv (must be evidence-backed; we skip incomplete)
    for p in REL.glob("*.csv"):
        for r in read_csv(p):
            src = (r.get("from_id") or "").strip()
            dst = (r.get("to_id") or "").strip()
            rel = (r.get("relation") or "").strip()
            if not (src and dst and rel):
                continue
            ev_ok = all((r.get(k) or "").strip() for k in ["source_title","source_locator","excerpt"])
            if not ev_ok:
                continue
            links.append({
                "source": src,
                "target": dst,
                "relation": rel,
                "evidence": {k: r.get(k,"") for k in EVIDENCE_FIELDS}
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"nodes": list(nodes.values()), "links": links}, indent=2), encoding="utf-8")
    print("Wrote:", OUT)
    print("Nodes:", len(nodes), "Links:", len(links))

if __name__ == "__main__":
    main()
