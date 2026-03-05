import subprocess

STEPS = [
    ("research ingest", "python /opt/atlas/scripts/research_ingest.py"),
    ("concepts",        "python /opt/atlas/scripts/concept_extract.py"),
    ("graph",           "python /opt/atlas/scripts/graph_viewer.py"),
]

def run():
    print("\nAtlas refresh\n")
    for name, cmd in STEPS:
        print(f"==> {name}")
        subprocess.run(cmd, shell=True)
    print("\nDone.\n")

if __name__ == "__main__":
    run()
