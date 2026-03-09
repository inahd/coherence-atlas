import json
import pathlib

p = pathlib.Path("memory/graphs/seed_graph.json")

if not p.exists():
    print("Graph file not found.")
    exit()

g = json.loads(p.read_text())

nodes = g.get("nodes", [])
edges = g.get("edges", [])

print("Nodes:", len(nodes))
print("Edges:", len(edges))
print()

print("First 10 nodes:")
for n in nodes[:10]:

    label = (
        n.get("label")
        or n.get("name")
        or n.get("id")
        or "unknown"
    )

    print("-", label)
