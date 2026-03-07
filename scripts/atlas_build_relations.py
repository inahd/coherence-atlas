import os
import json
import uuid

BASE_DIR = "/opt/atlas"
GRAPH_PATH = os.path.join(BASE_DIR, "data", "atlas_graph.json")
MAPPING_DIR = os.path.join(BASE_DIR, "datasets", "mappings")

# ---------------------------------------------------------
# Load graph
# ---------------------------------------------------------

with open(GRAPH_PATH) as f:
    graph = json.load(f)

entities = graph["entities"]
relations = graph["relations"]

name_to_id = {e["name"]: e["id"] for e in entities}

# ---------------------------------------------------------
# Create relation
# ---------------------------------------------------------

def create_relation(source, relation_type, target):

    return {
        "id": str(uuid.uuid4()),
        "source": name_to_id[source],
        "target": name_to_id[target],
        "relation_type": relation_type,

        "stability_layer": "working",

        "authority": {
            "shastra": 0.8,
            "sadhu": 0.7,
            "guru": 0.6
        },

        "visualization_permission": "relation"
    }

# ---------------------------------------------------------
# Process mapping files
# ---------------------------------------------------------

for file in os.listdir(MAPPING_DIR):

    if not file.endswith(".json"):
        continue

    path = os.path.join(MAPPING_DIR, file)

    with open(path) as f:
        data = json.load(f)

    relation_type = data["relation"]

    for pair in data["pairs"]:

        source, target = pair

        if source in name_to_id and target in name_to_id:

            relation = create_relation(source, relation_type, target)
            relations.append(relation)

# ---------------------------------------------------------
# Save graph
# ---------------------------------------------------------

with open(GRAPH_PATH, "w") as f:
    json.dump(graph, f, indent=2)

print("Relations built.")
print("Total relations:", len(graph["relations"]))
