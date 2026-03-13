#!/usr/bin/env python3

import sys
import json
import os

GRAPH_FILE = "/opt/atlas/data/graph.json"

def load_graph():
    if not os.path.exists(GRAPH_FILE):
        return {"nodes": [], "edges": []}
    with open(GRAPH_FILE) as f:
        return json.load(f)

def save_graph(graph):
    with open(GRAPH_FILE, "w") as f:
        json.dump(graph, f, indent=2)

def parse_input(lines):

    nodes = []
    edges = []

    for line in lines:

        parts = line.strip().split()

        if not parts:
            continue

        if parts[0] == "NODE":
            nodes.append({"type": parts[1], "name": parts[2]})

        if parts[0] == "EDGE":
            edges.append({
                "from": parts[1],
                "relation": parts[2],
                "to": parts[3]
            })

    return nodes, edges

def main():

    lines = sys.stdin.readlines()

    nodes,edges = parse_input(lines)

    graph = load_graph()

    graph["nodes"].extend(nodes)
    graph["edges"].extend(edges)

    save_graph(graph)

    print("\nAtlas graph updated")
    print("nodes:",len(nodes))
    print("edges:",len(edges))

if __name__ == "__main__":
    main()
