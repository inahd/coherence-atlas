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

# Deity nodes
add_node("Vayu",{"type":"deva","domain":"wind"})
add_node("Agni",{"type":"deva","domain":"fire"})
add_node("Soma",{"type":"deva","domain":"moon"})
add_node("Indra",{"type":"deva","domain":"storms"})
add_node("Yama",{"type":"deva","domain":"death"})
add_node("Varuna",{"type":"deva","domain":"cosmic_waters"})
add_node("Kubera",{"type":"deva","domain":"wealth"})
add_node("Hanuman",{"type":"avatar","domain":"devotion_strength"})

# Relationships

add_edge("Swati","deity","Vayu")
add_edge("Vayu","associated_with","Hanuman")

add_edge("Krittika","deity","Agni")
add_edge("Rohini","deity","Soma")
add_edge("Jyeshtha","deity","Indra")
add_edge("Bharani","deity","Yama")
add_edge("Shatabhisha","deity","Varuna")
add_edge("Dhanishta","deity","Kubera")

graph["nodes"]=nodes
graph["edges"]=edges

with open(GRAPH,"w") as f:
    yaml.dump(graph,f)

print("Deity layer added to Atlas graph.")
