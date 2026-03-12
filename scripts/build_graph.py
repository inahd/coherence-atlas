import json,sys,time

cutoff=None

if len(sys.argv)>1:
    cutoff=float(sys.argv[1])

nodes=set()
edges=[]

with open("ledger/events.jsonl") as f:
    for line in f:
        e=json.loads(line)

        if cutoff and e["timestamp"]>cutoff:
            continue

        if e["action"]=="propose_relation":
            nodes.add(e["from"])
            nodes.add(e["to"])

            edges.append({
                "from":e["from"],
                "rel":e["rel"],
                "to":e["to"],
                "status":e["status"]
            })

graph={"nodes":list(nodes),"edges":edges}

with open("projections/current_graph.json","w") as f:
    json.dump(graph,f,indent=2)

print("Graph rebuilt:",len(nodes),"nodes",len(edges),"edges")
