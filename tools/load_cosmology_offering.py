import json
import pathlib
from atlas.core.graph_store import save_graph

DATA = "data/cosmology/nakshatra_offering.json"
GRAPH = "memory/graphs/canonical_graph.json"

data = json.load(open(DATA, encoding="utf-8"))

graph = {"nodes": [], "edges": []}
path = pathlib.Path(GRAPH)

if path.exists():
    try:
        existing = json.load(open(GRAPH, encoding="utf-8"))
        graph["nodes"] = existing.get("nodes", [])
        graph["edges"] = existing.get("edges", existing.get("links", []))
    except Exception:
        pass

existing_nodes = {str(n.get("id")) for n in graph["nodes"]}

for n in data.get("nodes", []):
    if str(n.get("id")) not in existing_nodes:
        graph["nodes"].append(n)

graph["edges"].extend(data.get("edges", []))

save_graph(GRAPH, graph)

print("Cosmology offering accepted")
print("Nodes:", len(graph["nodes"]))
print("Edges:", len(graph["edges"]))
