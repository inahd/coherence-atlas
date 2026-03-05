import yaml, os

GRAPH="/opt/atlas/graph/graph.yaml"

nakshatra = [
("Ashwini","Ashwini Kumaras","Ketu"),
("Bharani","Yama","Venus"),
("Krittika","Agni","Sun"),
("Rohini","Brahma","Moon"),
("Mrigashira","Soma","Mars"),
("Ardra","Rudra","Rahu"),
("Punarvasu","Aditi","Jupiter"),
("Pushya","Brihaspati","Saturn"),
("Ashlesha","Nagas","Mercury"),
("Magha","Pitris","Ketu"),
("Purva Phalguni","Bhaga","Venus"),
("Uttara Phalguni","Aryaman","Sun"),
("Hasta","Savitar","Moon"),
("Chitra","Tvashtar","Mars"),
("Swati","Vayu","Rahu"),
("Vishakha","Indra-Agni","Jupiter"),
("Anuradha","Mitra","Saturn"),
("Jyeshtha","Indra","Mercury"),
("Mula","Nirriti","Ketu"),
("Purva Ashadha","Apas","Venus"),
("Uttara Ashadha","Vishvadevas","Sun"),
("Shravana","Vishnu","Moon"),
("Dhanishta","Vasus","Mars"),
("Shatabhisha","Varuna","Rahu"),
("Purva Bhadrapada","Aja Ekapada","Jupiter"),
("Uttara Bhadrapada","Ahirbudhnya","Saturn"),
("Revati","Pushan","Mercury")
]

graha=[
"Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"
]

rashi=[
"Aries","Taurus","Gemini","Cancer","Leo","Virgo",
"Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]

if os.path.exists(GRAPH):
    graph=yaml.safe_load(open(GRAPH))
else:
    graph={"nodes":{},"edges":[]}

nodes=graph["nodes"]
edges=graph["edges"]

for g in graha:
    nodes[g]={"type":"graha"}

for r in rashi:
    nodes[r]={"type":"rashi"}

for name,deity,ruler in nakshatra:

    nodes[name]={
        "type":"nakshatra",
        "deity":deity,
        "ruler":ruler
    }

    edges.append({"from":name,"to":ruler,"type":"ruled_by"})
    edges.append({"from":name,"to":deity,"type":"associated_deity"})

with open(GRAPH,"w") as f:
    yaml.dump(graph,f)

print("Atlas cosmic ontology generated.")
