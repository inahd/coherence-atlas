import json
import os
from pathlib import Path

ROOT = Path("/opt/atlas")
DATA = ROOT / "data"
OFFERINGS = ROOT / "atlas_codex" / "offerings"

def graph_stats():
    nodes = 0
    rels = 0

    for f in DATA.glob("*.json"):
        try:
            j = json.loads(open(f).read())
            if isinstance(j, dict):
                nodes += len(j.get("nodes", []))
                rels += len(j.get("links", []))
        except:
            pass

    return nodes, rels


def offerings_list():
    if not OFFERINGS.exists():
        return []

    files = sorted(OFFERINGS.glob("[0-9][0-9][0-9]_*.md"))
    result = []

    for f in files:
        num = f.name.split("_")[0]
        name = f.name.replace(".md","").split("_",1)[1].replace("_"," ").title()
        result.append(f"{num} {name}")

    return result


nodes, rels = graph_stats()
offerings = offerings_list()

readme = f"""
# Coherence Atlas

Atlas is a cosmological knowledge system connecting:

• cosmic cycles  
• ecology  
• human culture  
• sound and geometry  

---

## Current Graph State

Nodes: {nodes}  
Relations: {rels}

---

## Core Layers

Eternal Layer  
Cosmic Layer (Jyotish engine)  
Natural Layer (Ecology)  
Human Layer (Culture and practice)

---

## Key Systems

• Graph engine  
• Research ingestion pipeline  
• Cosmic swara generator  
• Mandala visualizations  
• CLI tools

---

## Codex Offerings
"""

for o in offerings:
    readme += f"\n{o}"

readme += "\n\n---\nGenerated automatically by Atlas."

open(ROOT / "README.md","w").write(readme)
print("README regenerated")

