import json, os
from pathlib import Path
import requests

BASE = Path("/opt/atlas")
STATE = BASE / "memory/reports/pb_state.json"
OUT = BASE / "memory/reports/next_pasteblock.sh"

OLLAMA_URL="http://127.0.0.1:11434"

def generate(prompt, model):
    r = requests.post(
        OLLAMA_URL + "/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120
    )
    r.raise_for_status()
    return r.json()["response"]

def main():

    if not STATE.exists():
        print("Missing:", STATE)
        return

    st = json.loads(STATE.read_text())

    SYSTEM = """
Generate a SAFE bash pasteblock that grows Atlas.

Goals:
- harvest more passages
- mine candidate relations
- resolve inference layers

Rules:
- never delete files
- never overwrite datasets
- operate inside /opt/atlas
Return only bash commands.
"""

    prompt = SYSTEM + "\nSTATE:\n" + json.dumps(st, indent=2)

    model = os.environ.get("OLLAMA_MODEL","phi3:latest")

    txt = generate(prompt, model)

    txt = txt.replace("```bash","").replace("```","").strip()

    OUT.write_text(txt + "\n")

    print("WROTE", OUT)
    print("---- preview ----")
    print("\n".join(txt.splitlines()[:20]))

if __name__ == "__main__":
    main()
