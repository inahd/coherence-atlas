import re
import pathlib

print("Atlas seed extractor starting...")

entities=set()

docs_path = pathlib.Path("docs")

if not docs_path.exists():
    print("No docs/ directory found.")
    exit()

text_files=list(docs_path.rglob("*.md"))

pattern = re.compile(r"([A-Z][a-z]+)")

for f in text_files:
    try:
        text=f.read_text()
    except:
        continue

    words=pattern.findall(text)

    for w in words:
        entities.add(w.lower())

print("Entities detected:",len(entities))

for e in sorted(entities):
    print(e)
