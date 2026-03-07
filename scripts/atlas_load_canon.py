import os
import json
import uuid

BASE_DIR = "/opt/atlas"
CANON_DIR = os.path.join(BASE_DIR, "datasets", "canonical")
GRAPH_PATH = os.path.join(BASE_DIR, "data", "atlas_graph.json")
PLACEHOLDER_PATH = os.path.join(BASE_DIR, "data", "placeholder_nodes.json")

# ---------------------------------------------------------
# Load graph
# ---------------------------------------------------------

if os.path.exists(GRAPH_PATH):
    with open(GRAPH_PATH) as f:
        graph = json.load(f)
else:
    graph = {"entities": [], "relations": []}

entities = graph["entities"]

# ---------------------------------------------------------
# Load placeholders
# ---------------------------------------------------------

if os.path.exists(PLACEHOLDER_PATH):
    with open(PLACEHOLDER_PATH) as f:
        placeholders = json.load(f)
else:
    placeholders = {"placeholders": []}

# ---------------------------------------------------------
# Helper: create canonical entity
# ---------------------------------------------------------

def create_canonical_entity(name, system):

    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "type": system,

        "stability_layer": "stable",

        "authority": {
            "shastra": 1.0,
            "sadhu": 0.7,
            "guru": 0.6
        },

        "visualization_permission": "symbolic"
    }

# ---------------------------------------------------------
# Helper: create placeholder
# ---------------------------------------------------------

def create_placeholder(system, expected_count, actual_count):

    return {
        "id": str(uuid.uuid4()),
        "name": f"{system}_missing_items",
        "type": "canonical_gap",
        "status": "placeholder",
        "gap_state": "needs_source",
        "expected_count": expected_count,
        "actual_count": actual_count
    }

# ---------------------------------------------------------
# Process canonical datasets
# ---------------------------------------------------------

for file in os.listdir(CANON_DIR):

    if not file.endswith(".json"):
        continue

    path = os.path.join(CANON_DIR, file)

    with open(path) as f:
        data = json.load(f)

    system = data["system"]
    items = data["items"]
    expected = data["expected_count"]

    existing_names = {e["name"] for e in entities}

    for name in items:

        if name not in existing_names:

            entity = create_canonical_entity(name, system)
            entities.append(entity)

    actual = len(items)

    if actual < expected:

        placeholder = create_placeholder(system, expected, actual)
        placeholders["placeholders"].append(placeholder)

# ---------------------------------------------------------
# Save graph
# ---------------------------------------------------------

with open(GRAPH_PATH, "w") as f:
    json.dump(graph, f, indent=2)

# ---------------------------------------------------------
# Save placeholders
# ---------------------------------------------------------

with open(PLACEHOLDER_PATH, "w") as f:
    json.dump(placeholders, f, indent=2)

print("Canonical structures loaded.")
print("Total entities:", len(graph["entities"]))
print("Placeholder gaps:", len(placeholders["placeholders"]))
