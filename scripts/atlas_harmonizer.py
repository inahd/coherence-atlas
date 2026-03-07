import os
import json
import uuid
from collections import defaultdict

BASE_DIR = "/opt/atlas"

GRAPH_PATH = os.path.join(BASE_DIR, "data", "atlas_graph.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "yantra_candidates.json")

# ---------------------------------------------------------
# Sacred number structures
# ---------------------------------------------------------

SACRED_NUMBERS = {
    3: "triangle",
    4: "square",
    5: "pentagon",
    6: "hexagon",
    8: "vastu_grid",
    9: "navagraha_mandala",
    12: "zodiac_wheel",
    27: "nakshatra_wheel"
}

# ---------------------------------------------------------
# Load graph
# ---------------------------------------------------------

with open(GRAPH_PATH) as f:
    graph = json.load(f)

entities = graph.get("entities", [])
relations = graph.get("relations", [])

# ---------------------------------------------------------
# Build adjacency
# ---------------------------------------------------------

adjacency = defaultdict(set)

for r in relations:
    adjacency[r["source"]].add(r["target"])
    adjacency[r["target"]].add(r["source"])

# ---------------------------------------------------------
# Detect clusters
# ---------------------------------------------------------

clusters = []

visited = set()

for entity in entities:

    eid = entity["id"]

    if eid in visited:
        continue

    neighbors = adjacency[eid]

    cluster = {eid}
    cluster.update(neighbors)

    visited.update(cluster)

    clusters.append(cluster)

# ---------------------------------------------------------
# Evaluate clusters
# ---------------------------------------------------------

candidates = []

for cluster in clusters:

    size = len(cluster)

    if size in SACRED_NUMBERS:

        geometry = SACRED_NUMBERS[size]

        candidate = {
            "id": str(uuid.uuid4()),
            "cluster_size": size,
            "geometry": geometry,
            "entity_ids": list(cluster),

            "stability_layer": "experimental",

            "authority": {
                "shastra": 0.0,
                "sadhu": 0.0,
                "guru": 0.5
            },

            "visualization_permission": "analytic"
        }

        candidates.append(candidate)

# ---------------------------------------------------------
# Save candidates
# ---------------------------------------------------------

with open(OUTPUT_PATH, "w") as f:
    json.dump(candidates, f, indent=2)

print("Yantra harmonizer complete.")
print("Candidates discovered:", len(candidates))
