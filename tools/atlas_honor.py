import json,os,glob

graph_file="memory/graphs/canonical_graph.json"
seed_dir="seeds"

if not os.path.exists(graph_file):
    print("No canonical graph found.")
    exit()

graph=json.load(open(graph_file))

nodes=graph.get("nodes",[])
edges=graph.get("edges",[])

existing_ids=set(n["id"] for n in nodes)

seed_files=glob.glob(seed_dir+"/*.md")

new_nodes=0

for f in seed_files:
    name=os.path.basename(f).replace(".md","")

    if name not in existing_ids:
        nodes.append({
            "id":name,
            "type":"seed",
            "source":f
        })
        new_nodes+=1

graph["nodes"]=nodes
graph["edges"]=edges

json.dump(graph,open(graph_file,"w"),indent=2)

print("Atlas honored offerings.")
print("New nodes:",new_nodes)
print("Total nodes:",len(nodes))
