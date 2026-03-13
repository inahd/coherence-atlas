import json

EXPLORER="/opt/atlas/memory/visualizations/atlas_graph_explorer.html"

html=open(EXPLORER).read()

controls="""
<div style="position:fixed;top:10px;left:10px;background:#111;color:#eee;padding:10px;font-family:monospace">
Atlas Layout<br>
<button onclick="setLayout('force')">Force</button>
<button onclick="setLayout('nakshatra')">Nakshatra</button>
<button onclick="setLayout('vastu')">Vastu</button>
<button onclick="setLayout('yantra')">Yantra</button>
</div>
"""

script="""
<script>
function setLayout(mode){

    if(mode==="force"){
        network.setOptions({physics:{enabled:true}})
    }

    if(mode==="vastu"){
        network.setOptions({physics:false})

        const coords={
            "NorthEast":[-200,-200],
            "North":[0,-200],
            "NorthWest":[200,-200],

            "East":[-200,0],
            "Center":[0,0],
            "West":[200,0],

            "SouthEast":[-200,200],
            "South":[0,200],
            "SouthWest":[200,200]
        }

        nodes.forEach(n=>{
            if(coords[n.id]){
                n.x=coords[n.id][0]
                n.y=coords[n.id][1]
                n.fixed=true
            }
        })

        network.setData({nodes:nodes,edges:edges})
    }

}
</script>
"""

if "Atlas Layout" not in html:

    html=html.replace("<body>","<body>"+controls+script)

open(EXPLORER,"w").write(html)

print("Layout modes installed")
