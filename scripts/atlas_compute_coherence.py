import json
import os
from collections import defaultdict

BASE_DIR = "/opt/atlas"

GRAPH_PATH = os.path.join(BASE_DIR,"data","atlas_graph.json")
OUTPUT_PATH = os.path.join(BASE_DIR,"data","coherence_scores.json")

# ---------------------------------------------------------
# Load graph
# ---------------------------------------------------------

with open(GRAPH_PATH) as f:
    graph = json.load(f)

entities = graph.get("entities",[])
relations = graph.get("relations",[])

# ---------------------------------------------------------
# Build adjacency
# ---------------------------------------------------------

connections = defaultdict(int)

for r in relations:
    connections[r["source"]] += 1
    connections[r["target"]] += 1

# ---------------------------------------------------------
# Coherence scoring
# ---------------------------------------------------------

scores = []

for e in entities:

    eid = e["id"]

    relation_score = connections[eid] * 0.1

    authority = e.get("authority",{})

    authority_score = (
        authority.get("shastra",0) * 0.5 +
        authority.get("sadhu",0) * 0.3 +
        authority.get("guru",0) * 0.2
    )

    coherence = relation_score + authority_score

    scores.append({
        "entity_id":eid,
        "name":e["name"],
        "coherence_score":round(coherence,3)
    })

# ---------------------------------------------------------
# Save scores
# ---------------------------------------------------------

with open(OUTPUT_PATH,"w") as f:
    json.dump(scores,f,indent=2)

print("Coherence analysis complete.")
print("Entities scored:",len(scores))
