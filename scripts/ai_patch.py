import sys
import requests
import difflib

OLLAMA_URL="http://localhost:11434/api/generate"
MODEL="phi3"

def ask_llm(prompt):

    print("Generating patch...")

    r=requests.post(
        OLLAMA_URL,
        json={"model":MODEL,"prompt":prompt,"stream":False},
        timeout=300
    )

    return r.json()["response"]

def improve(code):

    prompt=f"""
You are a senior Python engineer.

Improve this code while keeping the same functionality.

Focus on:
- clarity
- safety
- performance
- readability

Return ONLY the improved code.

Code:
{code}
"""

    return ask_llm(prompt)

def patch(path):

    with open(path,"r") as f:
        original=f.read()

    improved=improve(original)

    diff=difflib.unified_diff(
        original.splitlines(),
        improved.splitlines(),
        lineterm=""
    )

    print("\n".join(diff))

    confirm=input("\nApply patch? (y/n): ")

    if confirm.lower()=="y":
        with open(path,"w") as f:
            f.write(improved)
        print("Patch applied.")

if __name__=="__main__":

    if len(sys.argv)<2:
        print("Usage: atlas patch <file>")
        sys.exit()

    patch(sys.argv[1])
