import yaml
import sys

graph = yaml.safe_load(open("/opt/atlas/graph/graph.yaml"))

nodes = graph["nodes"]
edges = graph["edges"]

if len(sys.argv) < 2:
    print("usage: query_graph <node>")
    exit()

node = sys.argv[1]

if node in nodes:
    print(nodes[node])
else:
    print("node not found")

for e in edges:
    if e.get("from") == node:
        rel = e.get("relation") or e.get("type")
        print("->", rel, e.get("to"))
