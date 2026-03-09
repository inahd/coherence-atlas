import json, math, os

g=json.load(open("memory/graphs/atlas_merged_graph.json"))

nodes=g["nodes"]

width=1400
height=1000
cx=width//2
cy=height//2

rings=[120,260,420,560,720]

html="<html><body style='background:black;color:white'>"
html+=f"<canvas id=c width={width} height={height}></canvas>"
html+="<script>var ctx=c.getContext('2d');"

for i,n in enumerate(nodes):

    ring=min(i//60,len(rings)-1)
    r=rings[ring]

    a=i*0.17

    x=cx+math.cos(a)*r
    y=cy+math.sin(a)*r

    html+=f"ctx.beginPath();ctx.arc({x},{y},3,0,6.28);ctx.fill();"
    html+=f"ctx.fillText('{n['id']}',{x+6},{y});"

html+="</script></body></html>"

os.makedirs("memory/visualizations",exist_ok=True)

open("memory/visualizations/atlas_constellation.html","w").write(html)

print("constellation written")
print("nodes:",len(nodes))
