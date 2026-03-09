import json,math,os
g=json.load(open("memory/graphs/canonical_graph.json"))
nodes=g["nodes"]
html="<html><body style='background:black;color:white'><canvas id=c width=1000 height=800></canvas><script>"
html+="var ctx=c.getContext('2d');"
cx,cy=500,400
for i,n in enumerate(nodes):
    a=i*0.2
    x=cx+math.cos(a)*250
    y=cy+math.sin(a)*250
    html+=f"ctx.beginPath();ctx.arc({x},{y},4,0,6.28);ctx.fill();ctx.fillText('{n['id']}',{x+6},{y});"
html+="</script></body></html>"
os.makedirs("memory/visualizations",exist_ok=True)
open("memory/visualizations/atlas_mandala.html","w").write(html)
print("mandala generated")
