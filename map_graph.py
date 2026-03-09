#!/usr/bin/env python3

import json
from pyvis.network import Network

GRAPH_FILE = "/opt/atlas/data/graph.json"
OUT_FILE = "/opt/atlas/data/atlas_map.html"

with open(GRAPH_FILE) as f:
    graph = json.load(f)

net = Network(height="900px", width="100%", directed=True)

node_set = set()

# register explicit nodes
for node in graph["nodes"]:
    name = node["name"]
    node_set.add(name)
    net.add_node(name, label=name, title=node["type"])

# ensure nodes exist for edges
for edge in graph["edges"]:
    node_set.add(edge["from"])
    node_set.add(edge["to"])

for node in node_set:
    if node not in net.get_nodes():
        net.add_node(node, label=node)

# add edges
for edge in graph["edges"]:
    net.add_edge(edge["from"], edge["to"], label=edge["relation"])

net.show(OUT_FILE)

print("\nAtlas map generated:")
print(OUT_FILE)
