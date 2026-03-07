import json
import os
from collections import defaultdict

GRAPH="/opt/atlas/memory/cosmology_graph.json"
OUT_JSON="/opt/atlas/memory/patterns/pattern_clusters.json"
OUT_MD="/opt/atlas/docs/atlas_patterns.md"

def load_graph():
    if not os.path.exists(GRAPH):
        return {"nodes":[],"links":[]}
    return json.load(open(GRAPH))

g=load_graph()

nodes=g.get("nodes",[])
links=g.get("links",[])

adj=defaultdict(set)

for l in links:
    s=l.get("source")
    t=l.get("target")
    if s and t:
        adj[s].add(t)
        adj[t].add(s)

visited=set()
clusters=[]

for n in adj:
    if n in visited:
        continue
    stack=[n]
    cluster=set()

    while stack:
        cur=stack.pop()
        if cur in visited:
            continue

        visited.add(cur)
        cluster.add(cur)

        for nb in adj[cur]:
            if nb not in visited:
                stack.append(nb)

    clusters.append(cluster)

patterns=[]

for c in clusters:
    size=len(c)
    if size in [3,4,5,6,7,8,9,12,16,27]:
        patterns.append({
            "size":size,
            "nodes":sorted(list(c))
        })

os.makedirs("/opt/atlas/memory/patterns",exist_ok=True)

json.dump(patterns,open(OUT_JSON,"w"),indent=2)

with open(OUT_MD,"w") as f:

    f.write("# Atlas Pattern Report\n\n")
    f.write("Clusters that match sacred-number sizes\n\n")

    for p in patterns:
        f.write(f"## Cluster size {p['size']}\n")
        for n in p["nodes"][:30]:
            f.write(f"- {n}\n")
        f.write("\n")

print("Pattern report written:")
print(OUT_MD)
