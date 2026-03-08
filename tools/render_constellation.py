import json,math,random,os

data=json.load(open("atlas_graph/graph.json"))

nodes=data["nodes"]
edges=data["edges"]

width=900
height=700

pos={}

# distribute nodes in circle
for i,n in enumerate(nodes):
    angle=(i/len(nodes))*2*math.pi
    r=250
    x=width/2 + r*math.cos(angle)
    y=height/2 + r*math.sin(angle)
    pos[n["id"]] = (x,y)

html = "<html><body style='background:black;color:white;font-family:monospace'>"
html += f"<canvas id=c width={width} height={height}></canvas>"
html += "<script>var ctx=c.getContext('2d');"

# draw edges
for e in edges:
    if e["source"] in pos and e["target"] in pos:
        x1,y1 = pos[e["source"]]
        x2,y2 = pos[e["target"]]

        html += f"""
ctx.beginPath();
ctx.strokeStyle='rgba(200,200,255,0.3)';
ctx.moveTo({x1},{y1});
ctx.lineTo({x2},{y2});
ctx.stroke();
"""

# draw nodes
for name,(x,y) in pos.items():
    html += f"""
ctx.beginPath();
ctx.fillStyle='white';
ctx.arc({x},{y},5,0,6.28);
ctx.fill();
ctx.fillText("{name}",{x+8},{y+8});
"""

html += "</script></body></html>"

os.makedirs("visual",exist_ok=True)

open("visual/atlas_constellation.html","w").write(html)

print("Constellation rendered with edges.")
