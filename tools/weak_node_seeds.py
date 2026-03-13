import json
from collections import defaultdict
from pathlib import Path

GRAPH="memory/graphs/canonical_graph.json"
OUT="memory/research_seeds.json"

g=json.load(open(GRAPH))

nodes=g["nodes"]
edges=g["edges"]

degree=defaultdict(int)

for e in edges:
    degree[e["source"]] += 1
    degree[e["target"]] += 1

weak=[]

for n in nodes:
    nid=n.get("id") or n.get("name") or n.get("label")
    d=degree[nid]

    if d <= 1:
        weak.append({
            "node":nid,
            "degree":d,
            "seed":f"Investigate relationships of {nid}"
        })

out={
    "weak_nodes":len(weak),
    "seeds":weak[:50]
}

Path(OUT).write_text(json.dumps(out,indent=2))

print("Weak nodes:",len(weak))
print("Seeds written to:",OUT)
