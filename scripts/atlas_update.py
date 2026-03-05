import subprocess
import os

BASE="/opt/atlas"

def run(cmd):
    print("\nRunning:", cmd)
    subprocess.run(cmd, shell=True)

print("\n=== Atlas Update Pipeline ===\n")

# 1. Compute today's panchanga
panchanga = os.path.join(BASE,"scripts/panchanga.py")
if os.path.exists(panchanga):
    run(f"python {panchanga}")

# 2. Ensure graph exists
graph = os.path.join(BASE,"graph")
if not os.path.exists(graph):
    print("Creating graph directory")
    os.makedirs(graph)

# 3. Verify datasets
datasets = os.path.join(BASE,"datasets")
if os.path.exists(datasets):
    print("Datasets found:")
    for f in os.listdir(datasets):
        print("  ",f)

# 4. Journals
journal_dir = os.path.join(BASE,"journals")
os.makedirs(journal_dir,exist_ok=True)

print("\nAtlas update complete.\n")
