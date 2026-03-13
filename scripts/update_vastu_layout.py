import json

GRAPH="/opt/atlas/memory/cosmology_graph.json"
OUT="/opt/atlas/memory/visualizations/vastu_layout.json"

g=json.load(open(GRAPH))

# traditional vastu mandala coordinates
coords={
"NorthEast":(0,0),
"North":(1,0),
"NorthWest":(2,0),

"East":(0,1),
"Center":(1,1),
"West":(2,1),

"SouthEast":(0,2),
"South":(1,2),
"SouthWest":(2,2)
}

layout={}

for n in g.get("nodes",[]):

    name=n.get("id")

    if name in coords:

        x,y=coords[name]

        layout[name]={
            "x":x,
            "y":y,
            "type":"direction"
        }

json.dump(layout,open(OUT,"w"),indent=2)

print("Vastu layout generated:",OUT)
