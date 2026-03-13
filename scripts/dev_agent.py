import requests, json, os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
ROOT = "/opt/atlas"

SYSTEM = """
You are a coding assistant for a local project.
When asked to create or modify a file, respond in this format:

FILE: <relative/path/from/project/root>
CONTENT:
<full file content>

If the request is only an explanation, answer normally.
"""

def llm(prompt):
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False}
    )
    return r.json()["response"]

def apply_change(text):
    if "FILE:" not in text:
        print(text)
        return

    parts = text.split("FILE:")
    for p in parts[1:]:
        header, body = p.split("CONTENT:",1)
        path = header.strip()
        content = body.strip()

        full = os.path.join(ROOT, path)

        if not full.startswith(ROOT):
            print("Blocked path:", path)
            continue

        print("\nProposed change →", full)
        confirm = input("Apply? (y/n): ")

        if confirm.lower() == "y":
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full,"w") as f:
                f.write(content)
            print("Saved:", full)
        else:
            print("Skipped.")

def ask(q):
    prompt = SYSTEM + "\nUser: " + q
    resp = llm(prompt)
    apply_change(resp)

if __name__ == "__main__":
    print("Atlas Dev Agent")
    print("Creates or edits project files safely")
    print("Ctrl+C to exit\n")

    while True:
        try:
            q = input("agent> ")
            ask(q)
        except KeyboardInterrupt:
            print("\nExiting.")
            break
