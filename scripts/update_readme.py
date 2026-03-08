from pathlib import Path
import re

seed_dir = Path("seeds")

titles = []

for f in seed_dir.glob("*.md"):
    text = f.read_text()
    titles += re.findall(r"## (.+)", text)

section = "\n".join([f"- {t}" for t in titles])

readme = Path("README.md")
content = readme.read_text()

marker = "<!-- ATLAS_SEEDS -->"

if marker in content:
    pre,post = content.split(marker)
    new = pre + marker + "\n\n## Current Atlas Seeds\n\n" + section + "\n\n"
    readme.write_text(new)
    print("README updated.")
else:
    print("Seed marker not found in README.")
