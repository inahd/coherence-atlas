import json
import math

GRAPH = "/opt/atlas/memory/cosmology_graph.json"
OUT = "/opt/atlas/memory/visualizations/nakshatra_wheel.html"

import os
os.makedirs("/opt/atlas/memory/visualizations", exist_ok=True)

with open(GRAPH) as f:
    graph = json.load(f)

nodes = graph.get("nodes", [])

nakshatras = [n for n in nodes if n.get("type") == "nakshatra"]

count = len(nakshatras)

radius = 300
center = 400

html = """
<html>
<head>
<title>Nakshatra Wheel</title>
<style>
body { background:#000; color:#eee; font-family:monospace }
svg { border:1px solid #444 }
text { fill:#eee; font-size:12px }
circle { fill:#66ccff }
</style>
</head>
<body>

<h2>Atlas Nakshatra Wheel</h2>

<svg width="800" height="800">
"""

for i,n in enumerate(nakshatras):

    angle = (2*math.pi*i)/count

    x = center + radius * math.cos(angle)
    y = center + radius * math.sin(angle)

    name = n.get("id","?")

    html += f'<circle cx="{x}" cy="{y}" r="6"/>'
    html += f'<text x="{x+10}" y="{y+4}">{name}</text>'

html += """
</svg>
</body>
</html>
"""

with open(OUT,"w") as f:
    f.write(html)

print("Wheel written to:", OUT)
