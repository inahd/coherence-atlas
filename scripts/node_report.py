import json
import sys

GRAPH="/opt/atlas/memory/cosmology_graph.json"

node=sys.argv[1]

g=json.load(open(GRAPH))

print(f"\n=== NODE REPORT: {node} ===\n")

for link in g["links"]:
    if link["source"]==node:
        print(f"{node} -> {link['relation']} -> {link['target']}")
    if link["target"]==node:
        print(f"{link['source']} -> {link['relation']} -> {node}")
