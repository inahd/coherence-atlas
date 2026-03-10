
import csv
from pathlib import Path
from .graph_engine import Graph

def load_graph():

    g = Graph()

    nodes_file = Path("data/nodes.csv")
    rel_file = Path("data/relations.csv")

    if nodes_file.exists():
        with open(nodes_file) as f:
            for r in csv.DictReader(f):
                g.add_node(r["id"], r)

    if rel_file.exists():
        with open(rel_file) as f:
            for r in csv.DictReader(f):
                g.add_edge(r["from_id"], r["relation"], r["to_id"])

    return g
    
