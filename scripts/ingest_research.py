import os
import json
import re
from pathlib import Path

GRAPH_FILE = "/opt/atlas/memory/cosmology_graph.json"
RESEARCH_DIR = "/opt/atlas/research"

entity_patterns = {
    "Person": r"(Krishna|Arjuna|Parikshit|Kali|Gandhari|Krpa)",
    "Place": r"(Kurukshetra|Dvaraka|Indraprastha|Hastinapura|Kausambi)",
    "Concept": r"(Kali Age|Acintya Bhedabheda|Yantra|Mandala|Sri Yantra)"
}

def load_graph():
    if os.path.exists(GRAPH_FILE):
        with open(GRAPH_FILE) as f:
            return json.load(f)
    return {"nodes": [], "edges": []}

def save_graph(graph):
    with open(GRAPH_FILE, "w") as f:
        json.dump(graph, f, indent=2)

def detect_name_key(graph):
    if not graph["nodes"]:
        return "name"

    sample = graph["nodes"][0]

    for k in ["name","id","label"]:
        if k in sample:
            return k

    return "name"

def add_node(graph, name, ntype, key):
    for n in graph["nodes"]:
        if key in n and n[key].lower() == name.lower():
            return

    node = {key: name, "type": ntype}
    graph["nodes"].append(node)

def process_text(graph, text, key):
    for ntype, pattern in entity_patterns.items():
        for match in re.findall(pattern, text, re.IGNORECASE):
            add_node(graph, match, ntype, key)

def ingest():
    graph = load_graph()
    key = detect_name_key(graph)

    for file in Path(RESEARCH_DIR).glob("*"):
        if file.suffix.lower() in [".txt",".md"]:
            with open(file) as f:
                text = f.read()
                process_text(graph, text, key)

    save_graph(graph)

    print("Research ingested.")
    print("Total nodes:", len(graph["nodes"]))

if __name__ == "__main__":
    ingest()
