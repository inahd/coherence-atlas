import json, os, urllib.request

OLLAMA="http://127.0.0.1:11434/api/generate"

def ollama_generate(prompt, model):
    payload={
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options":{
            "num_predict":200,
            "temperature":0.3
        }
    }

    req=urllib.request.Request(
        OLLAMA,
        data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json"}
    )

    with urllib.request.urlopen(req,timeout=120) as r:
        return json.loads(r.read())["response"]


def main():

    model=os.environ.get("OLLAMA_MODEL","phi3:latest")

    SYSTEM="""
You are an AI architect for the Atlas cosmology knowledge graph.

Generate 5 concrete research or ingestion actions
that would expand the dataset.

Return them as a numbered list.
"""

    response=ollama_generate(SYSTEM,model)

    print("\n=== Atlas AI Plan ===\n")
    print(response)
    print("\n=====================\n")


if __name__=="__main__":
    main()
