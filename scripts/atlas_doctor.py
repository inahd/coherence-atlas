import yaml
import os

GRAPH="/opt/atlas/graph/graph.yaml"

if not os.path.exists(GRAPH):
    print("Graph not found")
    exit()

graph=yaml.safe_load(open(GRAPH))

nodes=graph.get("nodes",{})
edges=graph.get("edges",[])

print("Atlas Doctor Running...\n")

# --- Fix schema drift
fixed=0
for e in edges:
    if "type" in e and "relation" not in e:
        e["relation"]=e["type"]
        del e["type"]
        fixed+=1

if fixed:
    print("Fixed schema drift:",fixed,"edges")

# --- Remove duplicates
seen=set()
clean=[]
dup=0

for e in edges:
    key=(e["from"],e["relation"],e["to"])
    if key not in seen:
        clean.append(e)
        seen.add(key)
    else:
        dup+=1

edges=clean

if dup:
    print("Removed duplicate edges:",dup)

# --- Ensure nodes exist
missing=0
for e in edges:
    if e["from"] not in nodes:
        nodes[e["from"]]={"type":"concept"}
        missing+=1
    if e["to"] not in nodes:
        nodes[e["to"]]={"type":"concept"}
        missing+=1

if missing:
    print("Created missing nodes:",missing)

# --- Save graph
graph["nodes"]=nodes
graph["edges"]=edges

yaml.dump(graph,open(GRAPH,"w"))

# --- Stats
print("\nGraph Stats:")
print("Nodes:",len(nodes))
print("Edges:",len(edges))

print("\nAtlas graph healthy.")
