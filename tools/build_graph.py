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
