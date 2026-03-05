import csv, json
from pathlib import Path

BASE = Path("/opt/atlas")
DS = BASE / "datasets"
OUT = BASE / "memory" / "graphs" / "seed_graph.json"

REL_FILES = [
    DS / "relations_nakshatra_deity.csv",
    DS / "relations_devi_weapon.csv",
    DS / "relations_nakshatra_plants.csv",
    DS / "relations_ritual_calendar.csv",
    DS / "relations_raga_ritual.csv",
]

def read_csv(p: Path):
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def add_node(nodes, _id):
    if not _id:
        return
    if _id not in nodes:
        typ = _id.split(":", 1)[0] if ":" in _id else "unknown"
        nodes[_id] = {"id": _id, "type": typ, "name": _id}

def main():
    nodes = {}
    links = []

    for p in REL_FILES:
        for r in read_csv(p):
            src = (r.get("from_id") or "").strip()
            rel = (r.get("relation") or "").strip() or "related_to"
            dst = (r.get("to_id") or "").strip()

            # keep edge even if to_id missing
            if not dst:
                dst = f"todo:{rel}"

            if src:
                add_node(nodes, src)
                add_node(nodes, dst)
                links.append({
                    "source": src,
                    "target": dst,
                    "relation": rel,
                    "confidence": (r.get("confidence") or "seed_unverified").strip() or "seed_unverified"
                })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"nodes": list(nodes.values()), "links": links}, indent=2), encoding="utf-8")
    print("Wrote:", OUT)
    print("Nodes:", len(nodes), "Links:", len(links))

if __name__ == "__main__":
    main()
