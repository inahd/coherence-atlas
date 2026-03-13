import json
import time
import subprocess

METRICS="/opt/atlas/memory/yantra/atlas_coherence_metrics.json"
BRIDGE="/opt/atlas/memory/yantra/yantra_scope_bridge.json"

def export_metrics():
    subprocess.run(["python3","/opt/atlas/scripts/export_coherence_metrics.py"])

while True:

    export_metrics()

    data=json.load(open(METRICS))

    global_coherence=data.get("global_coherence",0)

    bridge={
        "symmetry": global_coherence,
        "chaos": 1-global_coherence,
        "iteration": int(5 + global_coherence*20),
        "phase": global_coherence
    }

    with open(BRIDGE,"w") as f:
        json.dump(bridge,f,indent=2)

    print("Yantra bridge updated:",bridge)

    time.sleep(10)
