import json
import re
from pathlib import Path

INPUT = Path("chat_import.txt")
OUT = Path("research/seeds/generated_seeds.json")

text = INPUT.read_text()

# simple pattern detection
keywords = [
    "quadrant",
    "cosmic cross",
    "nakshatra",
    "alchemy",
    "mandala",
    "field theory",
    "resonance",
    "symbol",
    "cycle"
]

seeds = []

for k in keywords:
    matches = re.findall(rf".{{0,80}}{k}.{{0,80}}", text, flags=re.I)
    for m in matches:
        seeds.append({
            "keyword": k,
            "context": m.strip()
        })

OUT.write_text(json.dumps(seeds, indent=2))

print("Generated", len(seeds), "candidate seeds.")
print("Saved to", OUT)
