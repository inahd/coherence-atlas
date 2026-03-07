import json, os, requests
from pathlib import Path

BASE = Path("/opt/atlas")

STATE_FILE = BASE / "memory/reports/pb_state.json"
OUT_FILE = BASE / "memory/reports/atlas_growth_plan.sh"

OLLAMA_URL = "http://127.0.0.1:11434"

def get_state():
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text())

def ask_model(prompt, model="phi3:latest"):
    r = requests.post(
        OLLAMA_URL + "/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    r.raise_for_status()

    return r.json()["response"]

def main():

    state = get_state()

    system_prompt = """
You are assisting the Atlas knowledge graph system.

Generate SAFE bash commands that help grow the system.

Goals:
- harvest text passages
- mine candidate relations
- improve inference layers

Rules:
- never delete files
- never overwrite datasets
- operate only inside /opt/atlas

Return ONLY bash commands.
"""

    prompt = system_prompt + "\nSTATE:\n" + json.dumps(state, indent=2)

    model = os.environ.get("OLLAMA_MODEL","phi3:latest")

    response = ask_model(prompt, model)

    response = response.replace("```bash","").replace("```","").strip()

    OUT_FILE.write_text(response + "\n")

    print("\nAtlas growth plan written to:")
    print(OUT_FILE)

    print("\nPreview:\n")
    print("\n".join(response.splitlines()[:20]))

if __name__ == "__main__":
    main()
