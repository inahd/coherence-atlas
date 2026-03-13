import json
import re
from pathlib import Path
from collections import defaultdict

GRAPH_PATH="memory/graphs/seed_graph.json"
DOCS_PATH="docs"

if not Path(GRAPH_PATH).exists():
    print("graph not found")
    exit()

graph=json.loads(Path(GRAPH_PATH).read_text())

nodes=graph.get("nodes",[])
edges=graph.get("edges",[])

node_labels=[n.get("name") or n.get("label") for n in nodes]

index=defaultdict(list)

for label in node_labels:
    key=label.lower()
    index[key].append(label)

pattern=re.compile(r"[A-Za-z_]+")

docs=list(Path(DOCS_PATH).rglob("*.md"))

for d in docs:
    text=d.read_text().lower()
    words=set(pattern.findall(text))
    
    for w in words:
        if w in index:
            for target in index[w]:
                edges.append({
                    "source":d.name,
                    "target":target,
                    "relation":"mentions"
                })

graph["edges"]=edges

Path(GRAPH_PATH).write_text(json.dumps(graph,indent=2))

print("edges generated:",len(edges))
