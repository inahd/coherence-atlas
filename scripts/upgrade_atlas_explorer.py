import re

EXPLORER="/opt/atlas/memory/visualizations/atlas_graph_explorer.html"

html=open(EXPLORER).read()

ui = """
<div style="position:fixed;right:10px;top:10px;width:260px;background:#111;color:#eee;
padding:10px;font-family:monospace;z-index:999">

<b>Atlas Explorer</b><br><br>

Search node:<br>
<input id="nodeSearch" style="width:100%" placeholder="Rohini / Agni / Vata">
<button onclick="searchNode()">Find</button>

<hr>

Node inspector:<br>
<div id="nodeInfo" style="height:200px;overflow:auto;background:#000;padding:5px">
click a node
</div>

</div>
"""

script = """
<script>

function searchNode(){

    const name=document.getElementById("nodeSearch").value.toLowerCase()

    const node=nodes.find(n=>n.id.toLowerCase().includes(name))

    if(!node){
        alert("Node not found")
        return
    }

    network.selectNodes([node.id])
    network.focus(node.id,{scale:1.5})
}

network.on("click",function(params){

    if(!params.nodes.length)return

    const id=params.nodes[0]

    let info="<b>"+id+"</b><br><br>"

    edges.forEach(e=>{
        if(e.from===id){
            info+=e.label+" → "+e.to+"<br>"
        }
        if(e.to===id){
            info+=e.label+" ← "+e.from+"<br>"
        }
    })

    document.getElementById("nodeInfo").innerHTML=info
})

</script>
"""

if "Atlas Explorer" not in html:

    html=html.replace("<body>","<body>"+ui+script)

open(EXPLORER,"w").write(html)

print("Atlas explorer upgraded")
