import requests
import subprocess
import json
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
SAFE_DIR = "/opt/atlas"

def stream_ai(prompt):
    r = requests.post(
        OLLAMA_URL,
        json={"model": "llama3", "prompt": prompt, "stream": True},
        stream=True
    )

    for line in r.iter_lines():
        if line:
            data = json.loads(line.decode())
            print(data.get("response",""), end="", flush=True)
    print("\n")

def run_cmd(cmd):
    return subprocess.getoutput(cmd)

def search_files(query):
    results=[]
    for root,dirs,files in os.walk(SAFE_DIR):
        for f in files:
            if query.lower() in f.lower():
                results.append(os.path.join(root,f))
    return "\n".join(results[:20]) or "No matches"

def read_file(path):
    try:
        if not path.startswith(SAFE_DIR):
            return "Access denied"
        with open(path) as f:
            return f.read()[:4000]
    except:
        return "Error reading file"

def handle(q):

    if q.startswith("run "):
        print(run_cmd(q[4:]))

    elif q.startswith("search "):
        print(search_files(q[7:]))

    elif q.startswith("read "):
        print(read_file(q[5:]))

    elif q.startswith("ai "):
        stream_ai(q[3:])

    else:
        print("Commands:")
        print(" ai <prompt>")
        print(" run <shell command>")
        print(" search <filename>")
        print(" read <file>")

if __name__ == "__main__":
    print("Atlas AI Dev Shell")
    print("Commands: ai | run | search | read")
    print("Ctrl+C to exit\n")

    while True:
        try:
            q=input("atlas> ")
            handle(q)
        except KeyboardInterrupt:
            print("\nExiting.")
            break
