import json
import networkx as nx
import os

DATA_FILE="/opt/atlas/data/cosmology.json"
GRAPH_FILE="/opt/atlas/memory/cosmology_graph.json"

def run():

    with open(DATA_FILE) as f:
        data=json.load(f)

    G=nx.Graph()

    for t in data["tithis"]:

        tithi=t["name"]
        devi=t["associated_devi"]

        G.add_node(tithi,type="tithi")
        G.add_node(devi,type="devi")

        G.add_edge(tithi,devi,relation="associated_devi")

        for w in t["weapons"]:
            G.add_node(w,type="weapon")
            G.add_edge(devi,w,relation="wields")

        for n in t["nakshatra_associations"]:
            G.add_node(n,type="nakshatra")
            G.add_edge(tithi,n,relation="associated_nakshatra")

        for m in t["music_associations"]:
            G.add_node(m,type="music")
            G.add_edge(tithi,m,relation="music_association")

    os.makedirs("/opt/atlas/memory",exist_ok=True)

    data=nx.node_link_data(G)

    with open(GRAPH_FILE,"w") as f:
        json.dump(data,f,indent=2)

    print("Cosmology graph built.")

if __name__=="__main__":
    run()
