import json
import os

BASE_DIR = "/opt/atlas"

GRAPH_PATH = os.path.join(BASE_DIR,"data","atlas_graph.json")
ALIAS_PATH = os.path.join(BASE_DIR,"schemas","entity_aliases.json")

# ---------------------------------------------------------
# Load files
# ---------------------------------------------------------

with open(GRAPH_PATH) as f:
    graph = json.load(f)

with open(ALIAS_PATH) as f:
    aliases = json.load(f)

entities = graph["entities"]

# ---------------------------------------------------------
# Build alias map
# ---------------------------------------------------------

alias_map = {}

for canonical,alts in aliases.items():

    alias_map[canonical.lower()] = canonical

    for a in alts:
        alias_map[a.lower()] = canonical

# ---------------------------------------------------------
# Normalize entity names
# ---------------------------------------------------------

seen = {}

for entity in entities:

    name = entity["name"]
    lower = name.lower()

    if lower in alias_map:

        canonical = alias_map[lower]
        entity["name"] = canonical

    # detect duplicates
    if entity["name"] in seen:
        entity["duplicate_of"] = seen[entity["name"]]
    else:
        seen[entity["name"]] = entity["id"]

# ---------------------------------------------------------
# Save graph
# ---------------------------------------------------------

with open(GRAPH_PATH,"w") as f:
    json.dump(graph,f,indent=2)

print("Entity normalization complete.")
