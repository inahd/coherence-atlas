import json
import pathlib
import itertools

graph_path = pathlib.Path("memory/graphs/seed_graph.json")

if not graph_path.exists():
    print("Graph not found")
    exit()

graph = json.loads(graph_path.read_text())

nodes = graph.get("nodes", [])
edges = []

for a, b in itertools.combinations(nodes, 2):

    edges.append({
        "source": a["id"],
        "target": b["id"],
        "type": "association"
    })

graph["edges"] = edges

graph_path.write_text(json.dumps(graph, indent=2))

print("Edges generated:", len(edges))
