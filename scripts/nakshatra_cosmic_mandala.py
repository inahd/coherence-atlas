import json
import math
import os

GRAPH="/opt/atlas/memory/cosmology_graph.json"
OUT="/opt/atlas/memory/visualizations/cosmic_mandala.html"

os.makedirs("/opt/atlas/memory/visualizations",exist_ok=True)

g=json.load(open(GRAPH))

nodes=g.get("nodes",[])
links=g.get("links",[])

nak=[n for n in nodes if n.get("type")=="nakshatra"]
gra=[n for n in nodes if n.get("type")=="graha"]

center=400

nak_r=300
gra_r=160

svg=[]

svg.append('<svg width="800" height="800" style="background:black">')

# compute positions
nak_pos={}
gra_pos={}

for i,n in enumerate(nak):
    ang=2*math.pi*i/len(nak)
    x=center+nak_r*math.cos(ang)
    y=center+nak_r*math.sin(ang)
    nak_pos[n["id"]]=(x,y)

for i,n in enumerate(gra):
    ang=2*math.pi*i/len(gra)
    x=center+gra_r*math.cos(ang)
    y=center+gra_r*math.sin(ang)
    gra_pos[n["id"]]=(x,y)

# draw lines
for l in links:
    if l["type"]=="nakshatra_ruler":
        s=l["source"]
        t=l["target"]

        if s in nak_pos and t in gra_pos:
            x1,y1=nak_pos[s]
            x2,y2=gra_pos[t]

            svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#444"/>')

# draw nakshatras
for name,(x,y) in nak_pos.items():
    svg.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#66ccff"/>')
    svg.append(f'<text x="{x+8}" y="{y+4}" fill="white" font-size="11">{name}</text>')

# draw grahas
for name,(x,y) in gra_pos.items():
    svg.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#ffcc66"/>')
    svg.append(f'<text x="{x+8}" y="{y+4}" fill="white" font-size="12">{name}</text>')

svg.append('</svg>')

html="""
<html>
<head>
<title>Atlas Cosmic Mandala</title>
</head>
<body style="background:black;color:white;font-family:monospace">
<h2>Atlas Cosmic Mandala</h2>
""" + "\n".join(svg) + "</body></html>"

open(OUT,"w").write(html)

print("Mandala written to:",OUT)
