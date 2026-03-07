import subprocess
import os

BASE = "/opt/atlas/scripts"

pipeline = [
    "atlas_load_canon.py",
    "atlas_ingest.py",
    "atlas_build_relations.py",
    "atlas_normalize_entities.py",
    "atlas_gap_detector.py",
    "atlas_build_research_queue.py",
    "atlas_execute_research.py",
    "atlas_harmonizer.py"
]

print("Starting Atlas pipeline...\n")

for step in pipeline:

    path = os.path.join(BASE, step)

    if not os.path.exists(path):
        print(f"Skipping {step} (missing)")
        continue

    print(f"Running {step}")

    subprocess.run(["python", path])

print("\nAtlas pipeline complete.")
