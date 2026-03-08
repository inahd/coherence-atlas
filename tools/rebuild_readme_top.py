from pathlib import Path

ROOT = Path(".")
README = ROOT/"README.md"

groups = {
"Core Docs":[],
"Software Tools":[],
"Reports":[]
}

if Path("docs").exists():
for p in Path("docs").glob("*.md"):
groups["Core Docs"].append(f"- [{p.stem}]({p})")

if Path("tools").exists():
for p in Path("tools").glob("*.py"):
groups["Software Tools"].append(f"- [{p.stem}]({p})")

if Path("memory/reports").exists():
for p in Path("memory/reports").glob("*"):
groups["Reports"].append(f"- [{p.stem}]({p})")

top = "# Coherence Atlas\n\n"
top += "## Navigation\n\n"

for g,l in groups.items():
if not l:
continue
top += f"\n### {g}\n\n"
top += "\n".join(l)+"\n"

## top += """

## Resonance Lattice

impetus
↓
cosmic context
↓
offering plate
↓
seed interpretation
↓
research lattice
↓
software + documentation + visualization
↓
next cycle
"""

body_marker="<!-- ATLAS_README_BODY -->"

if README.exists():
old=README.read_text()
else:
old=""

if body_marker in old:
body=old.split(body_marker,1)[1]
else:
body=old

README.write_text(top+"\n"+body_marker+"\n"+body)

print("README updated")
