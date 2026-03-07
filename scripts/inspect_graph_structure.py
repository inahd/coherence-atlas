import json
from collections import defaultdict

GRAPH="/opt/atlas/memory/cosmology_graph.json"

g=json.load(open(GRAPH))

nodes=g.get("nodes",[])
edges=g.get("links") or g.get("edges") or g.get("relations") or []

degree=defaultdict(int)

for e in edges:
    s=e.get("source")
    t=e.get("target")
    if s: degree[s]+=1
    if t: degree[t]+=1

print("\nTOTAL NODES:",len(nodes))
print("TOTAL EDGES:",len(edges))

print("\nMOST CONNECTED NODES:\n")

top=sorted(degree.items(), key=lambda x:x[1], reverse=True)

for node,count in top[:25]:
    print(f"{node:25} {count}")

print("\nNODE TYPES:\n")

types=defaultdict(int)

for n in nodes:
    types[n.get("type")]+=1

for t,c in sorted(types.items()):
    print(f"{t:15} {c}")

