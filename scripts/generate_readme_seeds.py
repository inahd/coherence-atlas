import os
from collections import defaultdict

SEED_DIR = "atlas/seeds"
OUTPUT_FILE = "docs/generated_seed_clusters.md"

clusters = defaultdict(list)

def parse_seed(filepath):
    data = {}
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                k,v = line.split(":",1)
                data[k.strip()] = v.strip()
    return data

if not os.path.exists(SEED_DIR):
    print("Seed directory not found.")
    exit()

for file in os.listdir(SEED_DIR):
    if file.endswith(".md"):
        seed = parse_seed(os.path.join(SEED_DIR,file))

        title = seed.get("TITLE","Unknown Seed")
        domain = seed.get("DOMAIN","misc")
        summary = seed.get("SUMMARY","")

        clusters[domain].append((title,summary))

with open(OUTPUT_FILE,"w",encoding="utf-8") as out:

    out.write("# Active Research Seeds\n\n")

    for domain,seeds in sorted(clusters.items()):
        out.write(f"## {domain}\n\n")

        for title,summary in seeds:
            out.write(f"- **{title}** — {summary}\n")

        out.write("\n")

print("README seed section generated:", OUTPUT_FILE)
