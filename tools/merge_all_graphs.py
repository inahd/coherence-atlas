import json
from pathlib import Path

ROOT = Path("/opt/atlas")

nodes = {}
edges = set()

def load_graph(path):
    try:
        data = json.loads(path.read_text())
    except:
        return

    if not isinstance(data, dict):
        return

    for n in data.get("nodes", []):
        nid = n.get("id") or n.get("name") or n.get("label")
        if nid:
            nodes[nid] = n

    for e in data.get("edges", []):
        src = e.get("source")
        tgt = e.get("target")
        rel = e.get("relation", "related_to")

        if src and tgt:
            edges.add((src, tgt, rel))


print("Scanning graphs...")

for f in ROOT.rglob("*.json"):
    if "graph" in f.name:
        load_graph(f)

print("Nodes collected:", len(nodes))
print("Edges collected:", len(edges))

out = {
    "nodes": list(nodes.values()),
    "edges": [
        {"source": s, "target": t, "relation": r}
        for s, t, r in edges
    ],
}

out_path = ROOT / "memory/graphs/canonical_graph.json"

out_path.write_text(json.dumps(out, indent=2))

print("\nAtlas canonical graph updated:")
print("Nodes:", len(out["nodes"]))
print("Edges:", len(out["edges"]))
