import os
import requests
from requests.exceptions import RequestException, Timeout
from dotenv import load_dotenv
from openai_client import ask as openai_ask

load_dotenv("/opt/atlas/.env")

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
LOCAL_MODEL = os.environ.get("ATLAS_LOCAL_MODEL", "phi3")
CLOUD_FALLBACK = os.environ.get("ATLAS_CLOUD_FALLBACK", "0") == "1"

def local_ask(prompt: str) -> str:
    r = requests.post(
        OLLAMA_URL,
        json={"model": LOCAL_MODEL, "prompt": prompt, "stream": False},
        timeout=60,
    )
    r.raise_for_status()
    return r.json().get("response", "")

def ask(prompt: str) -> str:
    prompt = prompt.strip()
    if prompt.startswith("/cloud "):
        return openai_ask(prompt[7:])

    try:
        return local_ask(prompt)
    except (RequestException, Timeout) as e:
        if CLOUD_FALLBACK:
            return openai_ask(prompt + f"\n\n[Local error: {e}]")
        raise

if __name__ == "__main__":
    print("atlas-chat> local by default; use `/cloud ...` for OpenAI")
    while True:
        q = input("atlas-chat> ").strip()
        if not q:
            continue
        print(ask(q))
