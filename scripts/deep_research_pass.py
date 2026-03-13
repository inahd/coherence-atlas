import re
from pathlib import Path
from collections import Counter

ROOT = Path("/opt/atlas")

SEARCH_DIRS = [
    "docs",
    "research",
    "research_archive",
    "wiki",
    "texts",
    "prompts",
    "seeds",
    "crawl/clean",
]

word_counts = Counter()

def extract_words(text):
    return re.findall(r"[A-Za-z]{4,}", text)

for d in SEARCH_DIRS:
    p = ROOT / d
    if not p.exists():
        continue

    for f in p.rglob("*"):
        if f.suffix.lower() in [".txt",".md",".json",".csv"]:
            try:
                text = f.read_text(errors="ignore")
                words = extract_words(text)

                for w in words:
                    word_counts[w.lower()] += 1

            except:
                pass

top_words = word_counts.most_common(200)

output = ROOT / "analysis" / "deep_research_terms.txt"
output.parent.mkdir(exist_ok=True)

with open(output,"w") as f:

    f.write("=== TOP TERMS IN ATLAS CORPUS ===\n\n")

    for word,count in top_words:
        f.write(f"{word:20} {count}\n")

print("Deep research report written to:", output)
import re
from pathlib import Path
from collections import Counter

ROOT = Path("/opt/atlas")

SEARCH_DIRS = [
    "docs",
    "research",
    "research_archive",
    "wiki",
    "texts",
    "prompts",
    "seeds",
    "crawl/clean",
]

word_counts = Counter()

def extract_words(text):
    return re.findall(r"[A-Za-z]{4,}", text)

for d in SEARCH_DIRS:
    p = ROOT / d
    if not p.exists():
        continue

    for f in p.rglob("*"):
        if f.suffix.lower() in [".txt",".md",".json",".csv"]:
            try:
                text = f.read_text(errors="ignore")
                words = extract_words(text)

                for w in words:
                    word_counts[w.lower()] += 1

            except:
                pass

top_words = word_counts.most_common(200)

output = ROOT / "analysis" / "deep_research_terms.txt"
output.parent.mkdir(exist_ok=True)

with open(output,"w") as f:

    f.write("=== TOP TERMS IN ATLAS CORPUS ===\n\n")

    for word,count in top_words:
        f.write(f"{word:20} {count}\n")

print("Deep research report written to:", output)
