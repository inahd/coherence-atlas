import yaml
import swisseph as swe
from datetime import datetime

GRAPH="/opt/atlas/graph/graph.yaml"

# load graph
graph=yaml.safe_load(open(GRAPH))
nodes=graph["nodes"]
edges=graph["edges"]

# compute panchanga
now=datetime.utcnow()
jd=swe.julday(now.year,now.month,now.day)

sun=swe.calc_ut(jd,swe.SUN)[0][0]
moon=swe.calc_ut(jd,swe.MOON)[0][0]

tithi=int(((moon-sun)%360)/12)+1
nak_index=int(moon/(360/27))

tithi_names=[
"Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami",
"Shashthi","Saptami","Ashtami","Navami","Dashami",
"Ekadashi","Dvadashi","Trayodashi","Chaturdashi","Purnima"
]

nakshatra_names=[
"Ashwini","Bharani","Krittika","Rohini","Mrigashira",
"Ardra","Punarvasu","Pushya","Ashlesha","Magha",
"PurvaPhalguni","UttaraPhalguni","Hasta","Chitra",
"Swati","Vishakha","Anuradha","Jyeshtha","Mula",
"PurvaAshadha","UttaraAshadha","Shravana","Dhanishta",
"Shatabhisha","PurvaBhadrapada","UttaraBhadrapada","Revati"
]

tithi_name=tithi_names[(tithi-1)%15]
nakshatra=nakshatra_names[nak_index]

print("Date:",now.strftime("%Y-%m-%d"))
print("Tithi:",tithi_name)
print("Nakshatra:",nakshatra)

print("\nMeaning:")

# interpret via graph
for e in edges:
    if e["from"]==nakshatra:
        print("Nakshatra relation:",e.get("relation", e.get("type","")),e["to"])

for e in edges:
    if e["from"]==tithi_name:
        print("Tithi relation:",e.get("relation", e.get("type","")),e["to"])
