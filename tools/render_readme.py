import os

def list_links(folder):
    if not os.path.exists(folder):
        return []
    items = sorted(os.listdir(folder))
    return [f"- `{folder}/{i}`" for i in items if not i.startswith(".")]

sections = {
    "Cosmology": list_links("architecture"),
    "Documentation": list_links("docs"),
    "Research Seeds": list_links("seeds"),
    "Software": list_links("tools"),
    "Visualizations": list_links("visual"),
    "Datasets": list_links("datasets"),
    "Experiments": list_links("experiments"),
}

header = """
# Coherence Atlas

*A living cosmology of knowledge.*

The **Coherence Atlas** explores relationships between cosmology,
Vedic knowledge systems, and modern computational structures.

Reality is modeled not as isolated facts but as a **field of relationships**.

---

## Atlas Portal
"""

body = ""

for name, items in sections.items():
    if not items:
        continue
    body += f"\n### {name}\n\n"
    body += "\n".join(items)
    body += "\n"

footer = """

---

## Resonance Cycle

Atlas grows through cycles:

impetus → seed → relations → constellation → insight → new seeds

Git commits mark the turning of the wheel.
"""

with open("README.md","w") as f:
    f.write(header + body + footer)

print("README regenerated.")
