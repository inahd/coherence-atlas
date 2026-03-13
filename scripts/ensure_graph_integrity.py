import json, os

GRAPH="/opt/atlas/memory/cosmology_graph.json"

def ensure_graph():
    if not os.path.exists(GRAPH):
        print("Graph missing — creating new graph")
        g={"nodes":[],"links":[]}
        os.makedirs(os.path.dirname(GRAPH),exist_ok=True)
        json.dump(g,open(GRAPH,"w"),indent=2)
        return

    g=json.load(open(GRAPH))
    changed=False

    if "nodes" not in g:
        g["nodes"]=[]
        changed=True

    if "links" not in g:
        g["links"]=[]
        changed=True

    if changed:
        json.dump(g,open(GRAPH,"w"),indent=2)
        print("Graph repaired")
    else:
        print("Graph OK")

ensure_graph()
