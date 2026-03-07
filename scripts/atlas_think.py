import os
import subprocess
from pathlib import Path

BASE = Path("/opt/atlas")
PLAN = BASE / "memory" / "cycle_plan.json"
PYTHON = "/opt/atlas/venv/bin/python"

def run(cmd):
    return subprocess.run(cmd, text=True)

def main():
    os.environ["OLLAMA_MODEL"] = os.environ.get("OLLAMA_MODEL", "phi3:latest")

    print("=== Atlas Think ===")
    print("Running planner...")
    rc = run([PYTHON, "/opt/atlas/scripts/ollama_plan.py"])
    if rc.returncode != 0:
        print("[ERROR] Planner failed.")
        raise SystemExit(rc.returncode)

    print("\n=== Saved Plan ===")
    if PLAN.exists():
        print(PLAN.read_text(encoding="utf-8", errors="ignore"))
    else:
        print("[WARN] No cycle_plan.json found.")

    print("\n=== Done ===")

if __name__ == "__main__":
    main()
