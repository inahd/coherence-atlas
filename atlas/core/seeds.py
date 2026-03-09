import pathlib
import json
import uuid

GRAPH="memory/graphs/seed_graph.json"
SEEDS_DIR=pathlib.Path("seeds")

def ingest():

    nodes=[]
    edges=[]

    for f in SEEDS_DIR.glob("*.md"):

        nid=str(uuid.uuid4())

        nodes.append({
            "id":nid,
            "label":f.stem,
            "type":"seed"
        })

    data={"nodes":nodes,"edges":edges}

    pathlib.Path(GRAPH).write_text(json.dumps(data,indent=2))

    print("Seeds ingested:",len(nodes))
