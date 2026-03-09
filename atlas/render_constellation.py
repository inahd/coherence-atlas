import json,math,os

g=json.load(open("memory/graphs/atlas_merged_graph.json"))

nodes=g.get("nodes",[])
edges=g.get("links",[])

width=1400
height=1000
cx=width//2
cy=height//2

html=f"""
<html>
<body style="background:black;color:white;font-family:monospace">
<h2>Atlas Constellation</h2>
Nodes: {len(nodes)} | Edges: {len(edges)}
<canvas id=c width={width} height={height}></canvas>
<script>
var ctx=c.getContext("2d");
ctx.fillStyle="white";
"""

for i,n in enumerate(nodes):

    ring=(i//60)+1
    r=ring*120

    angle=i*0.25

    x=cx+math.cos(angle)*r
    y=cy+math.sin(angle)*r

    html+=f"""
ctx.beginPath();
ctx.arc({x},{y},3,0,6.28);
ctx.fill();
ctx.fillText("{n['id']}",{x+5},{y});
"""

html+="</script></body></html>"

open("memory/visualizations/atlas_constellation.html","w").write(html)

print("rendered nodes:",len(nodes))
