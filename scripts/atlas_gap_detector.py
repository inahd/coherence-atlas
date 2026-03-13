import json
import uuid
import os

BASE_DIR = "/opt/atlas"

GRAPH_PATH = os.path.join(BASE_DIR, "data", "atlas_graph.json")
PLACEHOLDER_PATH = os.path.join(BASE_DIR, "data", "placeholder_nodes.json")

# --------------------------------
# Load graph
# --------------------------------

with open(GRAPH_PATH) as f:
    graph = json.load(f)

entities = graph.get("entities", [])

# --------------------------------
# Load placeholder registry
# --------------------------------

if os.path.exists(PLACEHOLDER_PATH):
    with open(PLACEHOLDER_PATH) as f:
        placeholders = json.load(f)
else:
    placeholders = {"placeholders": []}

# --------------------------------
# Helper: create placeholder
# --------------------------------

def create_placeholder(name, required_fields):

    node = {
        "id": str(uuid.uuid4()),
        "name": name,
        "type": "placeholder",
        "status": "placeholder",
        "gap_state": "unpopulated",
        "required_fields": required_fields
    }

    return node

# --------------------------------
# Gap detection rules
# --------------------------------

REQUIRED_ENTITY_FIELDS = [
    "stability_layer",
    "authority",
    "visualization_permission"
]

# --------------------------------
# Scan entities
# --------------------------------

new_placeholders = []

for entity in entities:

    missing = []

    for field in REQUIRED_ENTITY_FIELDS:

        if field not in entity:
            missing.append(field)

    if missing:

        placeholder = create_placeholder(
            f"missing_fields_for_{entity.get('name','unknown')}",
            missing
        )

        new_placeholders.append(placeholder)

# --------------------------------
# Append placeholders
# --------------------------------

placeholders["placeholders"].extend(new_placeholders)

with open(PLACEHOLDER_PATH, "w") as f:
    json.dump(placeholders, f, indent=2)

print("Gap scan complete.")
print("Placeholders created:", len(new_placeholders))
