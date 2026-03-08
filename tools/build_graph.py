import os, json, re

seed_dir = "seeds"
graph_file = "atlas_graph/graph.json"

nodes = []
edges = []

if not os.path.exists(seed_dir):
    os.makedirs(seed_dir)

for fname in os.listdir(seed_dir):
    path = os.path.join(seed_dir, fname)
    if not fname.endswith(".md"):
        continue

    node_id = fname.replace(".md","")
    nodes.append({"id":node_id,"type":"seed"})

    text=open(path).read()

    relations=re.findall(r"relations:(.*)",text)

    for r in relations:
        targets=[x.strip() for x in r.split(",") if x.strip()]
        for t in targets:
            edges.append({
                "source":node_id,
                "target":t,
                "type":"relates"
            })

graph={"nodes":nodes,"edges":edges}

os.makedirs("atlas_graph",exist_ok=True)

with open(graph_file,"w") as f:
    json.dump(graph,f,indent=2)

print("Atlas graph built.")
print("Nodes:",len(nodes))
print("Edges:",len(edges))
