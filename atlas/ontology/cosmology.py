import json

nodes=[]
edges=[]

def add_node(name,type_):
    nodes.append({"id":name,"type":type_})

def add_edge(a,rel,b):
    edges.append({"source":a,"relation":rel,"target":b})

# --- Graha

graha=[
"Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"
]

for g in graha:
    add_node(g,"graha")

# --- Rashi

rashi=[
"Aries","Taurus","Gemini","Cancer","Leo","Virgo",
"Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]

for r in rashi:
    add_node(r,"rashi")

# --- Nakshatra

nakshatra=[
"Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
"Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni",
"Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha",
"Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta",
"Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"
]

for n in nakshatra:
    add_node(n,"nakshatra")

# --- Example rulers (simplified classical sequence)

rulers=[
"Ketu","Venus","Sun","Moon","Mars","Rahu",
"Jupiter","Saturn","Mercury"
]

for i,n in enumerate(nakshatra):
    ruler=rulers[i%9]
    add_edge(n,"ruled_by",ruler)

# --- Pada

for n in nakshatra:
    for p in range(1,5):
        name=f"{n}_pada_{p}"
        add_node(name,"pada")
        add_edge(n,"has_pada",name)

# --- Write graph

graph={
"nodes":nodes,
"edges":edges
}

with open("memory/graphs/cosmology_graph.json","w") as f:
    json.dump(graph,f,indent=2)

print("Cosmology graph generated")
print("Nodes:",len(nodes))
print("Edges:",len(edges))
