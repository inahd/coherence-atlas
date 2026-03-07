import os
import json
from datetime import datetime

ROOT="/opt/atlas"
GRAPH=os.path.join(ROOT,"memory","cosmology_graph.json")
DATASETS=os.path.join(ROOT,"datasets")
SCRIPTS=os.path.join(ROOT,"scripts")

def safe_load_graph():
    if not os.path.exists(GRAPH):
        return {"nodes":[],"links":[]}
    with open(GRAPH) as f:
        return json.load(f)

def list_files(path,ext=None):
    out=[]
    for root,dirs,files in os.walk(path):
        for f in files:
            if ext and not f.endswith(ext):
                continue
            out.append(os.path.relpath(os.path.join(root,f),ROOT))
    return sorted(out)

graph=safe_load_graph()

nodes=graph.get("nodes",[])
edges=graph.get("links",[])

node_types=set()
for n in nodes:
    t=n.get("type")
    if t:
        node_types.add(t)

datasets=list_files(DATASETS,".csv")
scripts=list_files(SCRIPTS,".py")

state={
    "timestamp":datetime.utcnow().isoformat(),
    "nodes":len(nodes),
    "edges":len(edges),
    "node_types":sorted(list(node_types)),
    "datasets":datasets,
    "scripts":scripts
}

os.makedirs("docs",exist_ok=True)

with open("docs/atlas_state.json","w") as f:
    json.dump(state,f,indent=2)

md=[]
md.append("# Atlas Canon\n")
md.append(f"Generated: {state['timestamp']}\n")
md.append(f"Nodes: {state['nodes']}")
md.append(f"Edges: {state['edges']}\n")

md.append("## Node Types\n")
for t in state["node_types"]:
    md.append(f"- {t}")

md.append("\n## Datasets\n")
for d in state["datasets"]:
    md.append(f"- {d}")

md.append("\n## Scripts\n")
for s in state["scripts"]:
    md.append(f"- {s}")

with open("docs/atlas_canon.md","w") as f:
    f.write("\n".join(md))

print("Atlas Canon written:")
print(" docs/atlas_canon.md")
print(" docs/atlas_state.json")
