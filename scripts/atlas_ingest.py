import os
import csv
import json
import uuid

BASE_DIR = "/opt/atlas"
DATASET_DIR = os.path.join(BASE_DIR, "datasets")
OUTPUT_GRAPH = os.path.join(BASE_DIR, "data", "atlas_graph.json")
ENTITY_TYPES = os.path.join(BASE_DIR, "schemas", "entity_types.json")

# -----------------------------
# Load entity registry
# -----------------------------

with open(ENTITY_TYPES) as f:
    ENTITY_SCHEMA = json.load(f)["entity_types"]

# -----------------------------
# Graph structure
# -----------------------------

graph = {
    "entities": [],
    "relations": []
}

# -----------------------------
# Helper: create entity
# -----------------------------

def create_entity(name, entity_type, domain="general"):

    entity = {
        "id": str(uuid.uuid4()),
        "name": name,
        "type": entity_type,
        "domain": domain,

        "stability_layer": "experimental",

        "authority": {
            "shastra": 0.0,
            "sadhu": 0.0,
            "guru": 0.0
        },

        "visualization_permission": "relation"
    }

    return entity

# -----------------------------
# Helper: detect type
# -----------------------------

def detect_entity_type(name):

    lower = name.lower()

    if lower in ["fire","water","earth","air","ether"]:
        return "mahabhuta"

    if lower in ["vata","pitta","kapha"]:
        return "dosha"

    if lower in ["sattva","rajas","tamas"]:
        return "guna"

    return "substance"

# -----------------------------
# Dataset ingestion
# -----------------------------

def ingest_csv(path):

    with open(path) as f:
        reader = csv.reader(f)

        for row in reader:

            if not row:
                continue

            name = row[0].strip()

            entity_type = detect_entity_type(name)

            entity = create_entity(name, entity_type)

            graph["entities"].append(entity)

# -----------------------------
# Scan dataset directory
# -----------------------------

for root, dirs, files in os.walk(DATASET_DIR):

    for file in files:

        if file.endswith(".csv"):

            ingest_csv(os.path.join(root, file))

# -----------------------------
# Save graph
# -----------------------------

os.makedirs(os.path.dirname(OUTPUT_GRAPH), exist_ok=True)

with open(OUTPUT_GRAPH, "w") as f:
    json.dump(graph, f, indent=2)

print("Atlas ingestion complete.")
print("Entities:", len(graph["entities"]))
