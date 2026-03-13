import os,yaml,json,random

DATASETS="datasets"

entities={}
clusters={}
relations=[]

def load():
    for root,dirs,files in os.walk(DATASETS):
        for f in files:
            if f.endswith(".yaml") or f.endswith(".yml"):
                path=os.path.join(root,f)
                dataset=root.split("/")[-1]
                try:
                    data=yaml.safe_load(open(path))
                    if dataset not in clusters:
                        clusters[dataset]=[]
                    if isinstance(data,dict):
                        for k in data.keys():
                            entities[k]=dataset
                            clusters[dataset].append(k)
                    if isinstance(data,list):
                        for item in data:
                            if isinstance(item,dict):
                                for k in item.keys():
                                    entities[k]=dataset
                                    clusters[dataset].append(k)
                except:
                    pass

def infer_relations():
    keys=list(entities.keys())
    for a in keys:
        for b in keys:
            if a!=b and entities[a]!=entities[b]:
                if a.lower() in b.lower() or b.lower() in a.lower():
                    relations.append((a,b))

def write_reports():
    os.makedirs("memory/reports",exist_ok=True)

    with open("memory/reports/atlas_clusters.json","w") as f:
        json.dump(clusters,f,indent=2)

    with open("memory/reports/atlas_relations.json","w") as f:
        json.dump(relations,f,indent=2)

def build_cards():
    symbols=["☉","☾","♄","♃","♁","✶","✧","☸","🜁","🜂","🜃","🜄"]

    html="""
<html>
<head>
<title>Atlas Explorer</title>
<style>
body{background:#0e0e0e;color:white;font-family:sans-serif}
.grid{display:grid;grid-template-columns:repeat(auto-fill,200px);gap:20px;padding:40px}
.card{
background:#1f1f1f;
border:1px solid #444;
border-radius:10px;
padding:20px;
transition:0.3s;
cursor:pointer
}
.card:hover{background:#333;transform:scale(1.05)}
.symbol{font-size:32px;margin-bottom:10px}
.title{font-size:16px}
.cluster{font-size:11px;color:#aaa;margin-top:5px}
</style>
</head>
<body>
<h1 style="padding-left:40px">Atlas Cluster Explorer</h1>
<div class="grid">
"""

    for c in clusters:
        for name in clusters[c][:20]:
            html+=f"""
<div class="card">
<div class="symbol">{random.choice(symbols)}</div>
<div class="title">{name}</div>
<div class="cluster">{c}</div>
</div>
"""

    html+="</div></body></html>"

    os.makedirs("atlas_cards",exist_ok=True)
    open("atlas_cards/explorer.html","w").write(html)

def main():
    load()
    infer_relations()
    write_reports()
    build_cards()

    print("Entities:",len(entities))
    print("Relations inferred:",len(relations))
    print("Clusters:",len(clusters))
    print("Explorer: atlas_cards/explorer.html")

main()
