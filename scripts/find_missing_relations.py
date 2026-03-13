import json
import yaml
from collections import defaultdict

GRAPH="/opt/atlas/memory/cosmology_graph.json"
TEMPLATES="/opt/atlas/ontology/relation_templates.yaml"

with open(GRAPH) as f:
    graph=json.load(f)

with open(TEMPLATES) as f:
    templates=yaml.safe_load(f)

nodes=graph["nodes"]
edges=graph["links"]

node_relations=defaultdict(set)

for e in edges:
    node_relations[e["source"]].add(e["type"])

missing_report=[]

for n in nodes:

    ntype=n.get("type")

    if ntype not in templates:
        continue

    expected=templates[ntype]["relations"]

    expected_types=[list(x.keys())[0] for x in expected]

    existing=node_relations[n["id"]]

    missing=[r for r in expected_types if r not in existing]

    if missing:
        missing_report.append({
            "node":n["id"],
            "type":ntype,
            "missing":missing
        })

print("Nodes with missing ontology relations:",len(missing_report))

for r in missing_report[:50]:
    print(r)

