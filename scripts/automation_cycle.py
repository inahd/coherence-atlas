import json
import subprocess
from pathlib import Path

BASE = Path("/opt/atlas")
SCHEMA = BASE / "schemas" / "atlas_projection.json"
DATASETS = BASE / "datasets"
MEMORY = BASE / "memory"

SAFE_STEPS = [
    ("capsule_build", "atlas capsule_build"),
    ("concepts", "atlas concepts"),
    ("research", "atlas research"),
]

def run(cmd):
    return subprocess.run(cmd, shell=True)

def main():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    expected_rel = schema.get("relation_datasets_expected", [])

    # Determine “chores” from missing datasets + missing output artifacts
    chores = []

    missing_rel = [f for f in expected_rel if not (DATASETS / f).exists()]
    if missing_rel:
        chores.append({
            "type": "dataset_scaffold",
            "priority": "high",
            "action": "Create relation datasets (empty templates OK, but evidence columns required)",
            "items": missing_rel
        })

    if not (MEMORY / "vedic_cosmology_graph.json").exists():
        chores.append({
            "type": "build",
            "priority": "high",
            "action": "Run capsule_build to materialize canonical graph",
            "cmd": "atlas capsule_build"
        })

    # If concept graph exists but tiny, recommend adding corpus diversity (no automation)
    concepts = MEMORY / "concepts.json"
    if concepts.exists():
        try:
            g = json.loads(concepts.read_text(encoding="utf-8"))
            n_nodes = len(g.get("nodes", []))
            if n_nodes < 30:
                chores.append({
                    "type": "corpus_growth",
                    "priority": "medium",
                    "action": "Add more varied research sources (astro/ritual/plants/music). Then run atlas research + atlas concepts.",
                    "hint": "/opt/atlas/research/"
                })
        except Exception:
            pass
    else:
        chores.append({
            "type": "concepts",
            "priority": "medium",
            "action": "Run atlas concepts after you have some research files",
            "cmd": "atlas concepts"
        })

    # Write a plan file so it’s durable
    out = MEMORY / "cycle_plan.json"
    out.write_text(json.dumps({"chores": chores}, indent=2), encoding="utf-8")

    print("\nAutomation Cycle Plan (no canon invented)\n")
    for i, c in enumerate(chores, 1):
        print(f"{i}. [{c['priority']}] {c['type']}: {c['action']}")
        if "items" in c:
            for it in c["items"]:
                print("   -", it)
        if "cmd" in c:
            print("   cmd:", c["cmd"])
    print(f"\nWrote plan to: {out}\n")

    # Optional: run safe steps if requested
    # Usage: python automation_cycle.py --run
    import sys
    if "--run" in sys.argv:
        print("Running safe steps:\n")
        for name, cmd in SAFE_STEPS:
            print("==>", name, cmd)
            run(cmd)
        print("\nSafe run complete.\n")

if __name__ == "__main__":
    main()
