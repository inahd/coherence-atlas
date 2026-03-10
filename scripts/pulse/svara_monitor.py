#!/usr/bin/env python3

import time
import json
from pathlib import Path

ROOT = Path("/opt/atlas")
STATE = ROOT / "memory" / "pulse_state.json"

def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except:
            pass
    return {"cycle":0}

def save_state(s):
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(s,indent=2))

def main():

    state = load_state()

    state["cycle"] += 1
    state["last_tick"] = time.time()

    save_state(state)

    print()
    print("=== ATLAS SVARA PULSE ===")
    print("cycle:",state["cycle"])
    print("state file:",STATE)
    print()

if __name__ == "__main__":
    main()
