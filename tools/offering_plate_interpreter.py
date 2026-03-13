from pathlib import Path
import re

plate = Path("offerings/current/active_plate.md")

if not plate.exists():
    print("No active offering plate.")
    exit()

text = plate.read_text()

def section(name):
    m = re.search(rf"{name}:\n((?:- .*\n)+)", text)
    if not m:
        return []
    return [l[2:].strip() for l in m.group(1).splitlines()]

print("=== ACTIVE OFFERING ===")

fields = [
"COSMIC_CONTEXT",
"ACTIVE_SEEDS",
"RESEARCH_DIRECTIONS",
"SOFTWARE_DIRECTIONS",
"DATASET_DIRECTIONS",
"OUTPUT_DIRECTIONS"
]

for field in fields:
    print("\n"+field)
    for item in section(field):
        print(" -",item)
