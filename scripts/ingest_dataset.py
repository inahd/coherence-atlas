import yaml
import sys
import os

BASE="/opt/atlas"
DATASETS=os.path.join(BASE,"datasets")
GRAPH=os.path.join(BASE,"graph","graph.yaml")

dataset=sys.argv[1]

file=os.path.join(DATASETS,f"{dataset}.yaml")

if not os.path.exists(file):
    print("Dataset not found:",file)
    exit()

data=yaml.safe_load(open(file))

graph=yaml.safe_load(open(GRAPH))

nodes=graph.get("nodes",{})
edges=graph.get("edges",[])

def add_node(name,data):
    if name not in nodes:
        nodes[name]=data

def add_edge(a,rel,b):
    edge={"from":a,"relation":rel,"to":b}
    if edge not in edges:
        edges.append(edge)

# ingest nodes
for n in data.get("nodes",{}):
    add_node(n,data["nodes"][n])

# ingest edges
for e in data.get("edges",[]):
    add_edge(e["from"],e["relation"],e["to"])

graph["nodes"]=nodes
graph["edges"]=edges

with open(GRAPH,"w") as f:
    yaml.dump(graph,f)

print("Dataset ingested:",dataset)
