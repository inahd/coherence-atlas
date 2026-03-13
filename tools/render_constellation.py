import json, os, random

graph_file="memory/cosmology_graph.json"
out_file="visual/atlas_constellation.html"

g=json.load(open(graph_file))

nodes=g.get("nodes",[])
links=g.get("links",g.get("edges",[]))

html=f"""
<html>
<head>
<meta charset="utf-8">
<title>Atlas Constellation</title>
<style>
body {{background:black;color:white;font-family:monospace}}
canvas {{background:black}}
</style>
</head>
<body>
<h2>Atlas Constellation</h2>
<p>Nodes: {len(nodes)} | Edges: {len(links)}</p>
<canvas id="c" width="1200" height="800"></canvas>

<script>

const nodes={json.dumps(nodes)};
const edges={json.dumps(links)};

const canvas=document.getElementById("c");
const ctx=canvas.getContext("2d");

function rand(a,b){{return Math.random()*(b-a)+a}}

nodes.forEach(n=>{{
    n.x=rand(50,1150);
    n.y=rand(50,750);
}})

ctx.fillStyle="white"

nodes.forEach(n=>{{
    ctx.beginPath()
    ctx.arc(n.x,n.y,3,0,6.28)
    ctx.fill()
}})

ctx.strokeStyle="rgba(255,255,255,0.2)"

edges.forEach(e=>{{
    const a=nodes.find(n=>n.id==e.source)
    const b=nodes.find(n=>n.id==e.target)
    if(!a||!b)return

    ctx.beginPath()
    ctx.moveTo(a.x,a.y)
    ctx.lineTo(b.x,b.y)
    ctx.stroke()
}})

</script>
</body>
</html>
"""

os.makedirs("visual",exist_ok=True)
open(out_file,"w").write(html)

print("Constellation generated:",out_file)
print("Nodes:",len(nodes),"Edges:",len(links))
