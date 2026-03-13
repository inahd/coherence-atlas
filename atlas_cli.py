import os, sys, subprocess

def run(cmd):
    print(">>", cmd)
    subprocess.run(cmd, shell=True)

cmd = sys.argv[1] if len(sys.argv) > 1 else ""

if cmd == "doctor":
    run("python scripts/atlas_doctor.py")

elif cmd == "status":
    run("python scripts/status.py")

elif cmd == "report":
    run("python scripts/atlas_state_report.py")

elif cmd == "build":
    run("python scripts/rebuild_cosmology_graph.py")
    run("python scripts/ensure_graph_integrity.py")

elif cmd == "graph":
    run("python scripts/graph_viewer.py")

elif cmd == "wheel":
    run("python scripts/nakshatra_cosmic_wheel.py")

elif cmd == "mandala":
    run("python scripts/build_cosmic_mandala.py")

elif cmd == "research":
    run("python scripts/atlas_execute_research.py")

elif cmd == "deep":
    run("python scripts/deep_research_pass.py")

elif cmd == "cycle":
    run("python scripts/automation_cycle.py")

else:
    print("""
Atlas Control Commands

atlas doctor      → system diagnostics
atlas status      → quick system status
atlas report      → full atlas state report

atlas build       → rebuild cosmology graph
atlas graph       → open graph explorer
atlas wheel       → generate nakshatra wheel
atlas mandala     → generate cosmic mandala

atlas research    → run research expansion
atlas deep        → deep research pass
atlas cycle       → run automation cycle
""")
