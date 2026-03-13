import json
from pathlib import Path

GRAPH_CANDIDATES = [
    Path("memory/graphs/canonical_graph.json"),
    Path("memory/graphs/seed_graph.json"),
    Path("memory/graphs/cosmology_graph.json"),
]

def _normalize_graph(data, source=None):
    if not isinstance(data, dict):
        data = {}
    nodes = data.get("nodes", [])
    edges = data.get("edges", data.get("links", []))
    if not isinstance(nodes, list):
        nodes = []
    if not isinstance(edges, list):
        edges = []
    return {"nodes": nodes, "edges": edges, "_source": source}

def find_graph_path():
    for path in GRAPH_CANDIDATES:
        if path.exists():
            return path
    return None

def load_graph():
    path = find_graph_path()
    if path is None:
        return _normalize_graph({}, None)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return _normalize_graph({}, str(path))
    return _normalize_graph(data, str(path))

def save_graph(path_str, graph):
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    clean = {
        "nodes": graph.get("nodes", []),
        "edges": graph.get("edges", []),
    }
    path.write_text(json.dumps(clean, indent=2), encoding="utf-8")

def node_label(node):
    return (
        node.get("label")
        or node.get("name")
        or node.get("title")
        or node.get("id")
        or "node"
    )

def node_id(node):
    return str(node.get("id") or node_label(node))

def edge_type(edge):
    return edge.get("type") or edge.get("relation") or "related_to"
