import subprocess
import os
from pathlib import Path

RESEARCH = Path("/opt/atlas/research")

def run(cmd):
    print("Running:", cmd)
    subprocess.run(cmd, shell=True)

def main():

    if not RESEARCH.exists():
        print("No research folder found.")
        return

    print("Scanning research folder...")

    pdfs = list(RESEARCH.rglob("*.pdf"))
    txts = list(RESEARCH.rglob("*.txt"))

    print("PDF files:", len(pdfs))
    print("Text files:", len(txts))

    # extract text
    run("python scripts/pdftext_all.py")

    # extract passages
    run("python scripts/corpus_harvest_passages.py")

    # concept extraction
    run("python scripts/concept_extract.py")

    # ingest relations
    run("python scripts/ingest_relations_auto.py")

    # rebuild graph
    run("python scripts/rebuild_cosmology_graph.py")

    print("Atlas research ingestion complete.")

if __name__ == "__main__":
    main()
