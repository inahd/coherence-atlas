import json
import sys
from pathlib import Path

GRAPH_FILE = Path("/opt/atlas/memory/cosmology_graph.json")

def load_graph():
    if not GRAPH_FILE.exists():
        raise FileNotFoundError(f"Missing {GRAPH_FILE}. Run: atlas cosmology")
    return json.loads(GRAPH_FILE.read_text())

def neighbors_for(matches, links):
    related = set()
    for e in links:
        s = e.get("source")
        t = e.get("target")
        if s in matches:
            related.add(t)
        if t in matches:
            related.add(s)
    return related

def main():
    if len(sys.argv) < 2:
        print("Usage: atlas query <term>  OR  atlas query type:value")
        return

    raw = sys.argv[1]
    value = raw.split(":", 1)[1] if ":" in raw else raw
    value_l = value.lower()

    graph = load_graph()
    nodes = graph.get("nodes", [])
    links = graph.get("links", [])

    matches = []
    for n in nodes:
        node_id = str(n.get("id", ""))
        if value_l in node_id.lower():
            matches.append(node_id)

    related = neighbors_for(set(matches), links)

    print("\nMatches:\n")
    if matches:
        for m in matches:
            print(" ", m)
    else:
        print("  (none)")

    print("\nRelated:\n")
    if related:
        for r in sorted(related):
            print(" ", r)
    else:
        print("  (none)")

if __name__ == "__main__":
    main()
