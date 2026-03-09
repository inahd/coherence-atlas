import os
from pathlib import Path

ROOT = Path("/opt/atlas")

SEEDS = ROOT / "seeds"
AXIOMS = ROOT / "docs/axioms"
LOGS = ROOT / "logs"

README = ROOT / "README.md"


def list_items(path):
    if not path.exists():
        return []
    return sorted([p.stem for p in path.glob("*.md")])


def render_readme():

    seeds = list_items(SEEDS)
    axioms = list_items(AXIOMS)
    logs = list_items(LOGS)

    content = []

    content.append("# 🌱 Coherence Atlas\n")

    content.append("```\n")
    content.append("        🔱\n")
    content.append("        │\n")
    content.append("   🌱───🪷───🌱\n")
    content.append("        │\n")
    content.append("       ✨\n")
    content.append("```\n")

    content.append("## Atlas Cycle\n")
    content.append("🌱 seed → 🪷 relation → 🔱 principle → ✨ insight → 🌱 reseed\n")

    content.append("\n---\n")

    content.append("## 🌱 Seeds\n")
    if seeds:
        for s in seeds:
            content.append(f"- {s}\n")
    else:
        content.append("_none yet_\n")

    content.append("\n## 🔱 Axioms\n")
    if axioms:
        for a in axioms:
            content.append(f"- {a}\n")
    else:
        content.append("_none yet_\n")

    content.append("\n## ✨ Logs\n")
    if logs:
        for l in logs:
            content.append(f"- {l}\n")
    else:
        content.append("_none yet_\n")

    content.append("\n---\n")

    content.append("## Operator Loop\n")
    content.append("```\n")
    content.append("atlas seed <name>\n")
    content.append("atlas board\n")
    content.append("atlas tui\n")
    content.append("```\n")

    README.write_text("".join(content))


if __name__ == "__main__":
    render_readme()
