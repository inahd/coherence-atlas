import json
from collections import defaultdict, deque

GRAPH="/opt/atlas/memory/cosmology_graph.json"

g=json.load(open(GRAPH))

nodes=g.get("nodes",[])
edges=g.get("links") or g.get("edges") or g.get("relations") or []

graph=defaultdict(set)

for e in edges:
    s=e.get("source")
    t=e.get("target")
    if s and t:
        graph[s].add(t)
        graph[t].add(s)

visited=set()
clusters=[]

for node in graph:

    if node in visited:
        continue

    cluster=[]
    q=deque([node])
    visited.add(node)

    while q:

        n=q.popleft()
        cluster.append(n)

        for neigh in graph[n]:

            if neigh not in visited:
                visited.add(neigh)
                q.append(neigh)

    clusters.append(cluster)

clusters=sorted(clusters,key=len,reverse=True)

print("\nTOTAL CLUSTERS:",len(clusters))

print("\nLARGEST CLUSTERS:\n")

for i,c in enumerate(clusters[:10]):

    print(f"Cluster {i+1}  size={len(c)}")

    for n in c[:20]:
        print(" ",n)

    print()

