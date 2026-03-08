import json,math,random,os

g=json.load(open("atlas_graph/graph.json"))

nodes=g["nodes"]
edges=g["edges"]

pos={}

for n in nodes:
    a=random.random()*6.28
    r=200
    x=400+r*math.cos(a)
    y=300+r*math.sin(a)
    pos[n["id"]]=(x,y)

html="<html><body style='background:black;color:white'><canvas id=c width=800 height=600></canvas><script>var ctx=c.getContext('2d');"

for e in edges:
    if e["source"] in pos:
        x,y=pos[e["source"]]
        html+=f"ctx.fillStyle='white';ctx.fillText('{e['target']}',{x+5},{y+5});"

for n,(x,y) in pos.items():
    html+=f"ctx.beginPath();ctx.arc({x},{y},5,0,6.28);ctx.fill();ctx.fillText('{n}',{x+8},{y+8});"

html+="</script></body></html>"

os.makedirs("visual",exist_ok=True)

open("visual/atlas_constellation.html","w").write(html)

print("Constellation written to visual/atlas_constellation.html")
