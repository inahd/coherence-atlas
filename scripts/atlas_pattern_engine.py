import json
from collections import defaultdict

GRAPH="/opt/atlas/memory/cosmology_graph.json"

g=json.load(open(GRAPH))

nodes=g.get("nodes",[])
links=g.get("links",[])

degree=defaultdict(int)
neighbors=defaultdict(list)

for l in links:
    degree[l["source"]] += 1
    degree[l["target"]] += 1

    neighbors[l["source"]].append(l["target"])
    neighbors[l["target"]].append(l["source"])


print("\nAtlas Pattern Engine\n")

# ---- hub detection ----

print("Potential hub structures:\n")

for n in nodes:

    d=degree.get(n["id"],0)

    if d >= 6:

        print(" HUB:",n["id"],"connections:",d)


# ---- radial structures ----

print("\nRadial patterns:\n")

for n in nodes:

    neigh = neighbors[n["id"]]

    if len(neigh) >= 4:

        types=set()

        for m in neigh:
            for x in nodes:
                if x["id"]==m:
                    types.add(x.get("type"))

        if len(types) >= 3:

            print(" RADIAL:",n["id"],"neighbor_types:",list(types))


# ---- symmetry clusters ----

print("\nPossible symmetry clusters:\n")

cluster_map=defaultdict(list)

for n in nodes:

    d=degree.get(n["id"],0)

    cluster_map[d].append(n["id"])


for deg,group in cluster_map.items():

    if len(group) >= 3 and deg >=2:

        print(" DEGREE",deg,"cluster:",group[:10])


print("\nPattern scan complete\n")
