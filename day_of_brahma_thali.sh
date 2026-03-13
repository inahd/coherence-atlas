#!/usr/bin/env bash

echo "=== DAY OF BRAHMA THALI BEGIN ==="

mkdir -p architecture tools seeds memory/visualizations memory/graphs transcripts

echo "[1/5] Cosmology schema"

cat > architecture/atlas_cosmology_schema.md <<'SCHEMA'
# Atlas Cosmology Schema

Entity Types
Concept
CosmicBody
Cycle
Symbol
Structure
Person
Text
Place
Tool

Relation Types
belongs_to
manifests
governs
symbolizes
appears_in
part_of
activates
associated_with
SCHEMA

echo "[2/5] Seed explosion engine"

cat > tools/seed_explosion.py <<'PY'
import os,re
from datetime import datetime

SOURCE_DIRS=["docs","architecture","datasets","transcripts"]
SEED_DIR="seeds"
os.makedirs(SEED_DIR,exist_ok=True)

def topics(text):
    words=re.findall(r"[A-Za-z]{6,}",text.lower())
    freq={}
    for w in words:
        freq[w]=freq.get(w,0)+1
    return sorted(freq,key=freq.get,reverse=True)[:5]

for root in SOURCE_DIRS:
    if not os.path.exists(root): continue
    for f in os.listdir(root):
        p=os.path.join(root,f)
        if not os.path.isfile(p): continue
        text=open(p,errors="ignore").read()
        for t in topics(text):
            name=f"seed_{t}_{datetime.now().strftime('%H%M%S')}.md"
            open(os.path.join(SEED_DIR,name),"w").write(f"TITLE\n{t}\n")
PY

echo "[3/5] Graph builder"

cat > tools/build_graph.py <<'PY'
import os,json,re
nodes={}
edges=[]
for f in os.listdir("seeds"):
    text=open("seeds/"+f).read()
    m=re.search("TITLE\n(.+)",text)
    if not m: continue
    n=m.group(1).strip()
    nodes[n]={"id":n}
graph={"nodes":list(nodes.values()),"links":edges}
os.makedirs("memory/graphs",exist_ok=True)
json.dump(graph,open("memory/graphs/canonical_graph.json","w"),indent=2)
print("nodes:",len(nodes))
PY

echo "[4/5] Mandala renderer"

cat > tools/render_mandala.py <<'PY'
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
PY

echo "[5/5] Running cycle"

python tools/seed_explosion.py
python tools/build_graph.py
python tools/render_mandala.py

echo "=== DAY OF BRAHMA COMPLETE ==="
echo "Open:"
echo "firefox memory/visualizations/atlas_mandala.html"
