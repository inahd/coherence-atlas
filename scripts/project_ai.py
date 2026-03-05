import requests
import json
from vector_memory import search

OLLAMA_URL="http://localhost:11434/api/generate"

MODEL="llama3"

def ask_llm(prompt):

    r=requests.post(
        OLLAMA_URL,
        json={
            "model":MODEL,
            "prompt":prompt,
            "stream":True
        },
        stream=True
    )

    for line in r.iter_lines():
        if line:
            data=json.loads(line.decode())
            print(data.get("response",""),end="",flush=True)

    print("\n")

def ask(q):

    context=search(q)

    prompt=f"""
You are an AI assistant helping with a software project.

Relevant project files:
{context}

User question:
{q}

Answer based on the project context.
"""

    ask_llm(prompt)

if __name__=="__main__":

    print("Atlas Project AI")
    print("Uses vector memory to understand the repo")
    print("Ctrl+C to exit\n")

    while True:
        try:
            q=input("project-ai> ")
            ask(q)
        except KeyboardInterrupt:
            print("\nExiting.")
            break
