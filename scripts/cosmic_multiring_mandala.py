import json,math,os

GRAPH="/opt/atlas/memory/cosmology_graph.json"
OUT="/opt/atlas/memory/visualizations/cosmic_multiring_mandala.html"

os.makedirs("/opt/atlas/memory/visualizations",exist_ok=True)

g=json.load(open(GRAPH))

nodes=g["nodes"]
links=g["links"]

def get_nodes(t):
    return [n["id"] for n in nodes if n["type"]==t]

rings=[
("nakshatra",320,"#66ccff"),
("graha",260,"#ffcc66"),
("element",210,"#99ff99"),
("guna",170,"#ff99cc"),
("dosha",130,"#ff6666"),
]

center=400

svg=[]
svg.append('<svg width="800" height="800" style="background:black">')

positions={}

for t,r,color in rings:

    items=get_nodes(t)

    if not items:
        continue

    for i,name in enumerate(items):

        ang=2*math.pi*i/len(items)

        x=center+r*math.cos(ang)
        y=center+r*math.sin(ang)

        positions[name]=(x,y)

        svg.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}"/>')
        svg.append(f'<text x="{x+8}" y="{y+4}" fill="white" font-size="11">{name}</text>')


for l in links:

    s=l["source"]
    t=l["target"]

    if s in positions and t in positions:

        x1,y1=positions[s]
        x2,y2=positions[t]

        svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#444"/>')

svg.append('</svg>')

html="""
<html>
<head>
<title>Atlas Cosmic Mandala</title>
</head>
<body style="background:black;color:white;font-family:monospace">
<h2>Atlas Multi-Layer Cosmic Mandala</h2>
"""+"\n".join(svg)+"</body></html>"

open(OUT,"w").write(html)

print("Multiring mandala written to:",OUT)
