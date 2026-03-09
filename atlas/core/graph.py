import json
import pathlib

GRAPH_PATH = pathlib.Path("memory/graphs/seed_graph.json")

def load_graph():

    if not GRAPH_PATH.exists():
        return {"nodes":[],"edges":[]}

    return json.loads(GRAPH_PATH.read_text())

def node_count():
    g=load_graph()
    return len(g["nodes"])

def edge_count():
    g=load_graph()
    return len(g["edges"])
