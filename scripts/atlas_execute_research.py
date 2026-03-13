import os
import json

BASE_DIR = "/opt/atlas"

QUEUE_PATH = os.path.join(BASE_DIR, "data", "research_queue.json")
GRAPH_PATH = os.path.join(BASE_DIR, "data", "atlas_graph.json")

# ---------------------------------------------------------
# Load queue
# ---------------------------------------------------------

if os.path.exists(QUEUE_PATH):
    with open(QUEUE_PATH) as f:
        queue = json.load(f)
else:
    queue = []

# ---------------------------------------------------------
# Load graph
# ---------------------------------------------------------

if os.path.exists(GRAPH_PATH):
    with open(GRAPH_PATH) as f:
        graph = json.load(f)
else:
    graph = {"entities": [], "relations": []}

# ---------------------------------------------------------
# Simple automated resolution attempt
# ---------------------------------------------------------

def attempt_resolution(task):

    layer = task.get("layer")

    if layer == "stable":
        return "needs_manual_source"

    if layer == "working":
        return "needs_relation_discovery"

    if layer == "experimental":
        return "ai_analysis_candidate"

    return "unresolved"

# ---------------------------------------------------------
# Process tasks
# ---------------------------------------------------------

updated_queue = []

for task in queue:

    if task["status"] != "pending":
        updated_queue.append(task)
        continue

    result = attempt_resolution(task)

    task["status"] = result

    updated_queue.append(task)

# ---------------------------------------------------------
# Save queue
# ---------------------------------------------------------

with open(QUEUE_PATH, "w") as f:
    json.dump(updated_queue, f, indent=2)

print("Research executor complete.")
print("Tasks processed:", len(updated_queue))
