import json
import yaml

GRAPH="/opt/atlas/memory/cosmology_graph.json"
QUEUE="/opt/atlas/research_queue/queue.yaml"

with open(GRAPH) as f:
    graph=json.load(f)

tasks=[]

for e in graph["links"]:

    if "UNKNOWN_" in e["target"]:

        task={
            "id":"research_"+e["source"]+"_"+e["type"],
            "priority":"medium",
            "relation":e["type"],
            "node":e["source"],
            "target":e["target"]
        }

        tasks.append(task)

queue={"queue":tasks}

with open(QUEUE,"w") as f:
    yaml.dump(queue,f)

print("Research tasks generated:",len(tasks))
