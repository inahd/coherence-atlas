import math
import json
import pathlib

GRAPH_PATH = pathlib.Path("memory/graphs/seed_graph.json")

def load_graph():
    if not GRAPH_PATH.exists():
        return {"nodes": [], "edges": []}
    try:
        return json.loads(GRAPH_PATH.read_text())
    except:
        return {"nodes": [], "edges": []}

def node_label(n):

    if "label" in n:
        return n["label"]

    if "name" in n:
        return n["name"]

    if "id" in n:
        return str(n["id"])[:6]

    return "node"

def layout():

    g = load_graph()
    nodes = g.get("nodes", [])

    if not nodes:
        return []

    radius = 15
    positions = []

    for i,n in enumerate(nodes):

        angle = (i/len(nodes))*2*math.pi

        x=int(radius*math.cos(angle))
        y=int(radius*math.sin(angle))

        positions.append((node_label(n),x,y))

    return positions
