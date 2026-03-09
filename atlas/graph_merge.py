import json, os

CANONICAL = "memory/graphs/canonical_graph.json"
SEEDGRAPH = "memory/cosmology_graph.json"
OUT = "memory/graphs/atlas_merged_graph.json"

def load(p):
    if not os.path.exists(p):
        return {"nodes":[], "links":[]}
    return json.load(open(p))

a = load(CANONICAL)
b = load(SEEDGRAPH)

nodes={}
links=[]

for n in a.get("nodes",[])+b.get("nodes",[]):
    nodes[n["id"]] = n

for l in a.get("links",[])+b.get("links",[]):
    links.append(l)

g={
    "nodes": list(nodes.values()),
    "links": links
}

os.makedirs("memory/graphs",exist_ok=True)
json.dump(g,open(OUT,"w"),indent=2)

print("merged nodes:",len(g["nodes"]))
print("merged edges:",len(g["links"]))
