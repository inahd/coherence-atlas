import os
import subprocess
from pathlib import Path

def ok(name): print(f"[OK]   {name}")
def fail(name, msg=""): print(f"[FAIL] {name}" + (f" — {msg}" if msg else ""))

def cmd_exists(cmd):
    return subprocess.run(f"command -v {cmd} >/dev/null 2>&1", shell=True).returncode == 0

print("\nAtlas doctor\n")

# directories
for d in ["scripts", "data", "research", "memory"]:
    p = Path("/opt/atlas") / d
    ok(f"dir {p}") if p.exists() else fail(f"dir {p}", "missing")

# ollama
if cmd_exists("ollama"):
    ok("ollama binary")
    r = subprocess.run("curl -s http://localhost:11434 >/dev/null", shell=True)
    ok("ollama server") if r.returncode == 0 else fail("ollama server", "not reachable at :11434")
else:
    fail("ollama binary", "not installed/in PATH")

# key files
files = {
    "/opt/atlas/scripts/research_ingest.py": "research ingestion",
    "/opt/atlas/scripts/concept_extract.py": "concept extraction",
    "/opt/atlas/scripts/build_cosmology_graph.py": "cosmology graph builder",
}
for f, name in files.items():
    ok(name) if Path(f).exists() else fail(name, f"missing {f}")

# outputs
out = {
    "/opt/atlas/memory/concepts.json": "concept graph output",
    "/opt/atlas/memory/cosmology_graph.json": "cosmology graph output",
}
for f, name in out.items():
    ok(name) if Path(f).exists() else fail(name, f"missing {f} (run relevant command)")

print("")
