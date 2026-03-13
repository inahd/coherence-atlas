import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

data_dir = ROOT / "data"
readme_file = ROOT / "README.md"

nodes = 0
edges = 0

try:
    with open(data_dir / "atlas_graph.json") as f:
        g = json.load(f)
        nodes = len(g.get("nodes", []))
        edges = len(g.get("links", []))
except:
    pass

content = f"""
# Coherence Atlas

Atlas is a cosmological knowledge system connecting:

cosmic cycles  
ecology  
human culture  
sound and geometry  

---

## Current Graph State

Nodes: {nodes}  
Relations: {edges}

---

## Core Layers

Eternal Layer  
Cosmic Layer (Jyotish engine)  
Natural Layer (Ecology)  
Human Layer (Culture and practice)

---

## Key Systems

Graph engine  
Research ingestion pipeline  
Cosmic swara generator  
Mandala visualizations  
CLI tools

---

Generated automatically by Atlas.
"""

with open(readme_file, "w") as f:
    f.write(content.strip())

print("README generated:", readme_file)
