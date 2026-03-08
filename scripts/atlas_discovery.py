import os
import re
import json
from pathlib import Path
from collections import defaultdict

SEED_DIR = Path("seeds")
PROMPT_DIR = Path("prompts/generated")
REPORT_DIR = Path("memory/reports")

PROMPT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

term_index = defaultdict(list)
seeds = []

# read seeds
for f in SEED_DIR.glob("*.md"):
    text = f.read_text()
    seeds.append((f.name,text))

    words = re.findall(r'[A-Za-z]{5,}', text.lower())
    for w in set(words):
        term_index[w].append(f.name)

relations = []
clusters = defaultdict(list)

# detect overlaps
for term, files in term_index.items():
    if len(files) > 1:
        for f in files:
            clusters[f].append(term)

        relations.append({
            "term":term,
            "seeds":files
        })

# write cluster report
cluster_file = REPORT_DIR / "clusters.json"
with open(cluster_file,"w") as f:
    json.dump(clusters,f,indent=2)

# generate research prompts
prompts = []

for r in relations[:50]:
    seeds_join = ", ".join(r["seeds"])
    prompt = f"Investigate relation between {seeds_join} via concept '{r['term']}'."
    prompts.append(prompt)

prompt_file = PROMPT_DIR / "discovery_prompts.txt"
with open(prompt_file,"w") as f:
    f.write("\n".join(prompts))

print("Relations detected:",len(relations))
print("Prompts generated:",len(prompts))
