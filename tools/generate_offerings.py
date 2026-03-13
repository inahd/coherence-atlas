from pathlib import Path
from datetime import datetime
import re

plate = Path("offerings/current/active_plate.md")

if not plate.exists():
    print("No plate found.")
    exit()

text = plate.read_text()

def section(name):
    m = re.search(rf"{name}:\n((?:- .*\n)+)", text)
    if not m:
        return []
    return [l[2:].strip() for l in m.group(1).splitlines()]

items = (
    section("RESEARCH_DIRECTIONS") +
    section("SOFTWARE_DIRECTIONS") +
    section("OUTPUT_DIRECTIONS")
)

out = []

for item in items:
    out.append(f"""
## {item}

TYPE: emerging_offering
SOURCE: active_plate
NEXT_FORM: seed | module | visualization | documentation
""")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
target = Path(f"offerings/archive/offering_{stamp}.md")

target.write_text("# Generated Offerings\n\n" + "\n".join(out))

print(target)
