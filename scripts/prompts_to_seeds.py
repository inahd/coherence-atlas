import os
import re
from pathlib import Path

PROMPT_DIR = Path("prompts")
SEED_DIR = Path("seeds")

SEED_DIR.mkdir(exist_ok=True)

prompt_pattern = re.compile(r'(research|investigate|explore|relation|connection)', re.I)

count = 0

for file in PROMPT_DIR.glob("*.txt"):
    with open(file) as f:
        lines = f.readlines()

    seeds = []

    for line in lines:
        if prompt_pattern.search(line):

            title = line.strip()

            seed = f"""
## {title}

ENTRY DOMAIN:
unknown

TARGET DOMAIN:
unknown

ATTESTATION LEVEL:
EXPERIMENTAL

PROPOSED BRIDGE:
Prompt harvested from research log.

WHY THIS MATTERS:
Potential expansion of Atlas knowledge graph.
"""

            seeds.append(seed)

    if seeds:
        outfile = SEED_DIR / (file.stem + "_seeds.md")

        with open(outfile,"w") as f:
            f.write("# Harvested Atlas Seeds\n\n")
            f.writelines(seeds)

        count += len(seeds)

print(f"Harvested {count} seeds.")
