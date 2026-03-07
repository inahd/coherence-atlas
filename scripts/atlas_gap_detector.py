import json
from collections import defaultdict

GRAPH = "/opt/atlas/memory/cosmology_graph.json"

g = json.load(open(GRAPH))

nodes = g.get("nodes", [])
links = g.get("links", [])

print("\nAtlas Gap Detector\n")

# ---- connection counts ----

degree = defaultdict(int)

for l in links:
    degree[l["source"]] += 1
    degree[l["target"]] += 1

print("Weakly connected nodes:\n")

for n in nodes:
    d = degree.get(n["id"],0)
    if d <= 1:
        print(" ", n["id"], "(relations:", d,")")

# ---- relation type coverage ----

print("\nRelation type counts:\n")

rel_counts = defaultdict(int)

for l in links:
    rel_counts[l["type"]] += 1

for r,c in sorted(rel_counts.items()):
    print(" ", r, ":", c)

# ---- nodes missing type ----

print("\nNodes missing type:\n")

for n in nodes:
    if "type" not in n:
        print(" ", n["id"])

# ---- orphan nodes ----

print("\nOrphan nodes:\n")

for n in nodes:
    if degree.get(n["id"],0) == 0:
        print(" ", n["id"])

print("\nDone.\n")
