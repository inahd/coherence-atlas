import json
from collections import defaultdict

GRAPH="/opt/atlas/memory/cosmology_graph.json"

g=json.load(open(GRAPH))

nodes=g.get("nodes",[])
links=g.get("links",[])

degree=defaultdict(int)

for l in links:
    degree[l["source"]]+=1
    degree[l["target"]]+=1

tasks=[]

# weak nodes
for n in nodes:

    d=degree.get(n["id"],0)

    if d<=1:

        tasks.append({
            "priority":"high",
            "task":f"Expand relations for {n['id']}"
        })

# missing types
for n in nodes:

    if "type" not in n:

        tasks.append({
            "priority":"high",
            "task":f"Assign ontology type to {n['id']}"
        })

# sparse relation types
rel_counts=defaultdict(int)

for l in links:
    rel_counts[l["type"]]+=1

for r,c in rel_counts.items():

    if c<3:

        tasks.append({
            "priority":"medium",
            "task":f"Expand relation type '{r}'"
        })

queue={"queue":tasks}

OUT="/opt/atlas/research_queue/queue.json"

json.dump(queue,open(OUT,"w"),indent=2)

print("\nResearch queue generated\n")
print("Tasks:",len(tasks))
print("Output:",OUT)
