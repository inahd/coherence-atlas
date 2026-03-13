import csv,json,os

BASE="/opt/atlas"
DATA=BASE+"/datasets/cosmology"
OUT=BASE+"/memory/cosmology_graph.json"

nodes={}
links=[]

def node(name,t):
    key=(name,t)
    if key not in nodes:
        nodes[key]={"id":name,"type":t}

def link(a,b,t):
    links.append({"source":a,"target":b,"type":t})

# ---------- NAKSHATRA MASTER ----------

path=DATA+"/nakshatra_master.csv"

for r in csv.DictReader(open(path)):

    n=r["nakshatra"]

    node(n,"nakshatra")

    if r.get("element"):
        node(r["element"],"element")
        link(n,r["element"],"nakshatra_element")

    if r.get("guna"):
        node(r["guna"],"guna")
        link(n,r["guna"],"nakshatra_guna")

    if r.get("gana"):
        node(r["gana"],"gana")
        link(n,r["gana"],"nakshatra_gana")

    if r.get("dosha"):
        node(r["dosha"],"dosha")
        link(n,r["dosha"],"nakshatra_dosha")

    if r.get("yoni_animal"):
        node(r["yoni_animal"],"yoni")
        link(n,r["yoni_animal"],"nakshatra_yoni")

    if r.get("symbol"):
        node(r["symbol"],"symbol")
        link(n,r["symbol"],"nakshatra_symbol")

# ---------- NAKSHATRA DEITIES ----------

path=DATA+"/nakshatra_deities.csv"

if os.path.exists(path):
    for r in csv.DictReader(open(path)):
        n=r["nakshatra"]
        d=r["deity"]

        node(n,"nakshatra")
        node(d,"deity")

        link(n,d,"nakshatra_deity")

# ---------- GRAHA BIJA ----------

path=DATA+"/graha_bija.csv"

if os.path.exists(path):
    for r in csv.DictReader(open(path)):
        g=r["graha"]
        b=r["bija"]

        node(g,"graha")
        node(b,"bija")

        link(g,b,"graha_bija")

# ---------- WRITE GRAPH ----------

graph={
    "nodes":list(nodes.values()),
    "links":links
}

json.dump(graph,open(OUT,"w"),indent=2)

print("Graph rebuilt")
print("Nodes:",len(graph["nodes"]))
print("Links:",len(graph["links"]))
