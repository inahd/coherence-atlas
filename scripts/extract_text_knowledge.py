import yaml
import os
import re
import sys

GRAPH="/opt/atlas/graph/graph.yaml"

textfile=sys.argv[1]

if not os.path.exists(textfile):
    print("file not found")
    exit()

graph=yaml.safe_load(open(GRAPH))

nodes=graph.get("nodes",{})
edges=graph.get("edges",[])

def add_node(n):
    if n not in nodes:
        nodes[n]={"type":"concept"}

def add_edge(a,r,b):
    edge={"from":a,"relation":r,"to":b}
    if edge not in edges:
        edges.append(edge)

text=open(textfile).read()

# simple relationship extraction
patterns=[
(r"(\w+) is the deity of (\w+)","deity_of"),
(r"(\w+) rules (\w+)","rules"),
(r"(\w+) represents (\w+)","represents"),
(r"(\w+) wields (\w+)","wields")
]

for p,rel in patterns:
    for a,b in re.findall(p,text):
        add_node(a)
        add_node(b)
        add_edge(a,rel,b)

graph["nodes"]=nodes
graph["edges"]=edges

yaml.dump(graph,open(GRAPH,"w"))

print("knowledge extracted from text")
