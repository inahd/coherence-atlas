import yaml
from collections import defaultdict

GRAPH="/opt/atlas/graph/graph.yaml"
OUT="/opt/atlas/docs/"

graph=yaml.safe_load(open(GRAPH))

nodes=graph.get("nodes",{})
edges=graph.get("edges",[])

node_types=defaultdict(list)
relations=set()

for name,data in nodes.items():
    t=data.get("type","unknown")
    node_types[t].append(name)

for e in edges:
    r=e.get("relation",e.get("type","unknown"))
    relations.add(r)

# ensure docs folder exists
import os
os.makedirs(OUT,exist_ok=True)

# overview
with open(OUT+"atlas-overview.md","w") as f:
    f.write("# Atlas Knowledge Graph\n\n")
    f.write(f"Nodes: {len(nodes)}\n\n")
    f.write(f"Edges: {len(edges)}\n\n")

# node types
with open(OUT+"node-types.md","w") as f:
    f.write("# Node Types\n\n")
    for t,items in node_types.items():
        f.write(f"## {t}\n\n")
        for i in sorted(items):
            f.write(f"- {i}\n")
        f.write("\n")

# relation types
with open(OUT+"relation-types.md","w") as f:
    f.write("# Relation Types\n\n")
    for r in sorted(relations):
        f.write(f"- {r}\n")

print("Atlas documentation generated.")
