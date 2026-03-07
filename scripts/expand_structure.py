import json
import yaml

GRAPH="/opt/atlas/memory/cosmology_graph.json"
TEMPLATES="/opt/atlas/ontology/relation_templates.yaml"

graph=json.load(open(GRAPH))
templates=yaml.safe_load(open(TEMPLATES))

nodes=graph.get("nodes",[])

# detect correct edge container
edges = graph.get("links") or graph.get("edges") or graph.get("relations")

# if none exists, create one
if edges is None:
    edges=[]
    graph["edges"]=edges

existing=set()

for e in edges:
    existing.add((e.get("source"),e.get("target"),e.get("type")))

new_edges=[]

for n in nodes:

    ntype=n.get("type")

    if ntype not in templates:
        continue

    rels=templates[ntype]["relations"]

    for rel in rels:

        rtype=list(rel.keys())[0]
        target_type=rel[rtype]

        key=(n["id"],"UNKNOWN_"+target_type,rtype)

        if key not in existing:

            new_edges.append({
                "source":n["id"],
                "target":"UNKNOWN_"+target_type,
                "type":rtype
            })

edges.extend(new_edges)

# ensure graph saves edges consistently
if "links" in graph:
    graph["links"]=edges
elif "relations" in graph:
    graph["relations"]=edges
else:
    graph["edges"]=edges

json.dump(graph,open(GRAPH,"w"),indent=2)

print("Structural relations added:",len(new_edges))
