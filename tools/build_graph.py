import os, json, re

seed_dir = "seeds"
graph_file = "atlas_graph/graph.json"

nodes=[]
edges=[]

for fname in os.listdir(seed_dir):
    if not fname.endswith(".md"):
        continue

    node_id=fname.replace(".md","")
    nodes.append({"id":node_id,"type":"seed"})

    text=open(os.path.join(seed_dir,fname)).read()

    rel=re.findall(r"relations:(.*)",text)

    for r in rel:
        for t in [x.strip() for x in r.split(",") if x.strip()]:
            edges.append({
                "source":node_id,
                "target":t,
                "type":"relates"
            })

graph={"nodes":nodes,"edges":edges}

os.makedirs("atlas_graph",exist_ok=True)

with open(graph_file,"w") as f:
    json.dump(graph,f,indent=2)

print("Graph built.")
print("Nodes:",len(nodes))
print("Edges:",len(edges))
