import os
import json
import uuid

BASE_DIR = "/opt/atlas"

PLACEHOLDER_PATH = os.path.join(BASE_DIR, "data", "placeholder_nodes.json")
GRAPH_PATH = os.path.join(BASE_DIR, "data", "atlas_graph.json")
QUEUE_PATH = os.path.join(BASE_DIR, "data", "research_queue.json")

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

if os.path.exists(PLACEHOLDER_PATH):
    with open(PLACEHOLDER_PATH) as f:
        placeholders = json.load(f)["placeholders"]
else:
    placeholders = []

if os.path.exists(GRAPH_PATH):
    with open(GRAPH_PATH) as f:
        graph = json.load(f)
else:
    graph = {"entities": [], "relations": []}

# ---------------------------------------------------------
# Task scoring
# ---------------------------------------------------------

def compute_priority(gap_state):

    weights = {
        "needs_source": 0.9,
        "needs_authority": 0.8,
        "needs_relation": 0.7,
        "needs_review": 0.5,
        "partial": 0.4,
        "unpopulated": 0.3
    }

    return weights.get(gap_state, 0.2)

# ---------------------------------------------------------
# Determine research layer
# ---------------------------------------------------------

def determine_layer(gap_type):

    if "canonical" in gap_type:
        return "stable"

    if "relation" in gap_type:
        return "working"

    return "experimental"

# ---------------------------------------------------------
# Build tasks
# ---------------------------------------------------------

tasks = []

for node in placeholders:

    task = {
        "task_id": str(uuid.uuid4()),
        "target": node["name"],
        "gap_state": node.get("gap_state","unpopulated"),
        "layer": determine_layer(node.get("type","data_gap")),
        "priority": compute_priority(node.get("gap_state","unpopulated")),
        "status": "pending"
    }

    tasks.append(task)

# ---------------------------------------------------------
# Sort tasks by priority
# ---------------------------------------------------------

tasks = sorted(tasks, key=lambda x: x["priority"], reverse=True)

# ---------------------------------------------------------
# Save queue
# ---------------------------------------------------------

with open(QUEUE_PATH, "w") as f:
    json.dump(tasks, f, indent=2)

print("Research queue built.")
print("Tasks:", len(tasks))
