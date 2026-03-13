import csv
from pathlib import Path

ROOT = Path("/opt/atlas")
README = ROOT / "README.md"
REL = ROOT / "data/relations.csv"

START = "<!-- ATLAS_CONSTELLATION_START -->"
END = "<!-- ATLAS_CONSTELLATION_END -->"

def load_nodes():
    nodes = []
    if REL.exists():
        with REL.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                a = row.get("from_id", "").strip()
                b = row.get("to_id", "").strip()
                if a:
                    nodes.append(a)
                if b:
                    nodes.append(b)
    nodes = sorted(set(nodes))
    fallback = ["plants", "jyotish", "ayurveda", "symbolic", "research"]
    for x in fallback:
        if x not in nodes:
            nodes.append(x)
    return nodes[:5]

def build_constellation(nodes):
    a, b, c, d, e = nodes[:5]
    return (
        "```text\n"
        f"                ✶ {a}\n"
        "                    │\n"
        f"      {b} ── relation ── {c}\n"
        "                    │\n"
        f"                {d}\n"
        "                    │\n"
        f"                 {e}\n"
        "```\n"
    )

def update_readme(block_text):
    if README.exists():
        text = README.read_text(encoding="utf-8")
    else:
        text = "# Coherence Atlas\n\n"
    block = f"{START}\n{block_text}\n{END}"
    if START in text and END in text:
        before = text.split(START)[0]
        after = text.split(END, 1)[1]
        text = before + block + after
    else:
        text += "\n## Atlas Constellation\n\n" + block + "\n"
    README.write_text(text, encoding="utf-8")

def main():
    nodes = load_nodes()
    block = build_constellation(nodes)
    update_readme(block)
    print("Atlas constellation updated.")
    print("Nodes used:", ", ".join(nodes))

if __name__ == "__main__":
    main()
