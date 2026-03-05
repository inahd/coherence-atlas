import yaml

file="/opt/atlas/graph/graph.yaml"

g=yaml.safe_load(open(file))

nodes=g["nodes"]
edges=g["edges"]

qualities={
"Ashwini":["healing","speed","beginnings"],
"Bharani":["transformation","discipline","restraint"],
"Krittika":["fire","purification","cutting"],
"Rohini":["growth","fertility","beauty"],
"Mrigashira":["seeking","curiosity","wandering"],
"Ardra":["storm","intensity","change"],
"Punarvasu":["renewal","return","restoration"],
"Pushya":["nourishment","support","prosperity"],
"Ashlesha":["serpent","coiling","mystery"],
"Magha":["ancestors","authority","heritage"],
"Purva Phalguni":["pleasure","creativity","union"],
"Uttara Phalguni":["contracts","friendship","stability"],
"Hasta":["craft","skill","hands"],
"Chitra":["beauty","design","architecture"],
"Swati":["wind","independence","movement"],
"Vishakha":["focus","achievement","duality"],
"Anuradha":["friendship","devotion","cooperation"],
"Jyeshtha":["power","seniority","protection"],
"Mula":["roots","destruction","investigation"],
"Purva Ashadha":["invincibility","water","purification"],
"Uttara Ashadha":["victory","truth","endurance"],
"Shravana":["listening","learning","transmission"],
"Dhanishta":["rhythm","music","prosperity"],
"Shatabhisha":["healing","mystery","seclusion"],
"Purva Bhadrapada":["intensity","vision","asceticism"],
"Uttara Bhadrapada":["depth","stability","patience"],
"Revati":["prosperity","nurturing","travel"]
}

for n,qs in qualities.items():

    for q in qs:

        qnode="quality_"+q

        if qnode not in nodes:
            nodes[qnode]={"type":"quality","name":q}

        edges.append({
            "from":n,
            "to":qnode,
            "type":"has_quality"
        })

yaml.dump(g,open(file,"w"))

print("Nakshatra qualities added.")
