import subprocess

STEPS = [
    ("research ingest", "python /opt/atlas/scripts/research_ingest.py"),
    ("vector memory",   "python /opt/atlas/scripts/vector_memory.py"),
    ("concept extract", "python /opt/atlas/scripts/concept_extract.py"),
    ("cosmology graph", "python /opt/atlas/scripts/build_cosmology_graph.py"),
]

def run():
    print("\nAtlas build pipeline\n")
    for name, cmd in STEPS:
        print(f"==> {name}: {cmd}")
        subprocess.run(cmd, shell=True, check=False)
    print("\nPipeline complete.\n")

if __name__ == "__main__":
    run()
