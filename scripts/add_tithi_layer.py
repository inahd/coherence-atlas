import yaml
import os

GRAPH="/opt/atlas/graph/graph.yaml"

if not os.path.exists(GRAPH):
    print("Graph not found:", GRAPH)
    exit()

graph=yaml.safe_load(open(GRAPH))

nodes=graph.get("nodes",{})
edges=graph.get("edges",[])

def add_node(name,data):
    if name not in nodes:
        nodes[name]=data

def add_edge(a,rel,b):
    edges.append({
        "from":a,
        "relation":rel,
        "to":b
    })

# Tithi nodes
tithis=[
"Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami",
"Shashthi","Saptami","Ashtami","Navami","Dashami",
"Ekadashi","Dvadashi","Trayodashi","Chaturdashi","Purnima"
]

for t in tithis:
    add_node(t,{"type":"tithi"})

# Major associations
add_node("Ganesha",{"type":"deva"})
add_node("Durga",{"type":"devi"})
add_node("Vishnu",{"type":"deva"})
add_node("Shiva",{"type":"deva"})
add_node("Lakshmi",{"type":"devi"})

add_edge("Chaturthi","associated_deity","Ganesha")
add_edge("Ashtami","associated_deity","Durga")
add_edge("Ekadashi","associated_deity","Vishnu")
add_edge("Trayodashi","associated_deity","Shiva")
add_edge("Purnima","associated_deity","Lakshmi")

graph["nodes"]=nodes
graph["edges"]=edges

with open(GRAPH,"w") as f:
    yaml.dump(graph,f)

print("Tithi layer added to Atlas.")
