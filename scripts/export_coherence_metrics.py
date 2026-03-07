import json
import yaml
from collections import defaultdict
import os

GRAPH="/opt/atlas/memory/cosmology_graph.json"
TEMPLATES="/opt/atlas/ontology/relation_templates.yaml"
OUT="/opt/atlas/memory/yantra/atlas_coherence_metrics.json"

graph=json.load(open(GRAPH))
templates=yaml.safe_load(open(TEMPLATES))

nodes=graph.get("nodes",[])
edges=graph.get("links") or graph.get("edges") or graph.get("relations") or []

node_relations=defaultdict(set)

for e in edges:
    src=e.get("source")
    typ=e.get("type")
    if src and typ:
        node_relations[src].add(typ)

layer_stats=defaultdict(lambda: {"total":0,"filled":0})

for n in nodes:

    nid=n.get("id")
    ntype=n.get("type")

    if ntype not in templates:
        continue

    expected=templates[ntype]["relations"]
    expected_types=[list(x.keys())[0] for x in expected]

    existing=node_relations.get(nid,set())

    filled=len([r for r in expected_types if r in existing])

    layer_stats[ntype]["total"]+=len(expected_types)
    layer_stats[ntype]["filled"]+=filled

metrics={}

global_total=0
global_filled=0

for layer,data in layer_stats.items():

    if data["total"]==0:
        continue

    coherence=data["filled"]/data["total"]

    metrics[layer]=round(coherence,3)

    global_total+=data["total"]
    global_filled+=data["filled"]

metrics["global"]=round(global_filled/global_total,3) if global_total else 0

os.makedirs("/opt/atlas/memory/yantra",exist_ok=True)

json.dump(metrics,open(OUT,"w"),indent=2)

print("Layered coherence metrics exported:")
print(metrics)
