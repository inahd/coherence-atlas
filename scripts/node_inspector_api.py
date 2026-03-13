import json,os
from flask import Flask,jsonify

GRAPH="/opt/atlas/memory/cosmology_graph.json"

app=Flask(__name__)

def load_graph():
    if not os.path.exists(GRAPH):
        return {"nodes":[],"links":[]}

    try:
        g=json.load(open(GRAPH))
    except:
        return {"nodes":[],"links":[]}

    if "nodes" not in g:
        g["nodes"]=[]
    if "links" not in g:
        if "edges" in g:
            g["links"]=g["edges"]
        else:
            g["links"]=[]

    return g

@app.route("/health")
def health():
    g=load_graph()
    return jsonify({
        "ok":True,
        "nodes":len(g["nodes"]),
        "links":len(g["links"])
    })

@app.route("/node/<path:n>")
def node(n):
    g=load_graph()

    nodes={x.get("id"):x for x in g["nodes"]}
    edges=g["links"]

    rel=[]

    for e in edges:
        s=e.get("source") or e.get("from")
        t=e.get("target") or e.get("to")
        typ=e.get("type","related")

        if s==n:
            rel.append({"type":typ,"target":t})
        elif t==n:
            rel.append({"type":typ,"target":s})

    return jsonify({
        "node":nodes.get(n),
        "relations":rel
    })

if __name__=="__main__":
    app.run(host="127.0.0.1",port=7011)
