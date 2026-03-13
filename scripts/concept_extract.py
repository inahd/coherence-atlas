import os, json, re, requests, networkx as nx

RESEARCH_DIR="/opt/atlas/research"
GRAPH_FILE="/opt/atlas/memory/concepts.json"

OLLAMA_URL="http://localhost:11434/api/generate"
MODEL="phi3"

MAX_FILES = 8
MAX_CHARS = 1200
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 25  # total per file ~30s

def extract_json(text):
    m = re.search(r'\{.*\}', text, flags=re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except:
        return None

def ask_llm_stream(prompt):
    # stream=True so we can show progress; (connect, read) timeouts
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": True},
        stream=True,
        timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
    )
    buf = []
    for line in r.iter_lines():
        if not line:
            continue
        try:
            obj = json.loads(line.decode("utf-8"))
            chunk = obj.get("response", "")
            if chunk:
                buf.append(chunk)
        except:
            # ignore malformed lines
            continue
    return "".join(buf)

def extract_from_text(doc_text):
    prompt = (
        "Return ONLY valid JSON. No markdown.\n"
        "{\n"
        '  "concepts": ["..."],\n'
        '  "relations": [["A","B","related_to"], ...]\n'
        "}\n"
        "Rules: 3-10 concepts max. relations optional.\n\n"
        "TEXT:\n" + doc_text[:MAX_CHARS]
    )
    raw = ask_llm_stream(prompt)
    return extract_json(raw)

def run():
    G = nx.Graph()
    files = []
    for root, _, fs in os.walk(RESEARCH_DIR):
        for f in fs:
            files.append(os.path.join(root, f))
    files = sorted(files)[:MAX_FILES]

    if not files:
        print("No files in /opt/atlas/research")
        return

    print(f"Concept extract: {len(files)} file(s), model={MODEL}, timeouts=({CONNECT_TIMEOUT},{READ_TIMEOUT})\n")

    for i, path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {path}")
        try:
            with open(path, "r", errors="ignore") as fh:
                text = fh.read()
        except Exception as e:
            print("  SKIP read error:", e)
            continue

        print("  querying model...", end="", flush=True)
        try:
            data = extract_from_text(text)
            print(" done")
        except requests.exceptions.ReadTimeout:
            print(" TIMEOUT (read) — skipped")
            continue
        except requests.exceptions.ConnectTimeout:
            print(" TIMEOUT (connect) — is Ollama running? skipped")
            continue
        except Exception as e:
            print(f" ERROR — {e}")
            continue

        if not data:
            print("  PARSE FAIL (no JSON) — skipped")
            continue

        concepts = [str(c).strip() for c in (data.get("concepts") or []) if str(c).strip()]
        relations = data.get("relations") or []

        for c in concepts:
            G.add_node(c)

        for r in relations:
            if isinstance(r, list) and len(r) >= 2:
                a = str(r[0]).strip()
                b = str(r[1]).strip()
                rel = str(r[2]).strip() if len(r) >= 3 else "related_to"
                if a and b:
                    G.add_edge(a, b, relation=rel)

        print(f"  OK (+{len(concepts)} concepts, +{len(relations)} relations)")

    os.makedirs("/opt/atlas/memory", exist_ok=True)
    with open(GRAPH_FILE, "w") as out:
        json.dump(nx.node_link_data(G), out, indent=2)

    print(f"\nSaved {GRAPH_FILE}")
    print("Total:", G.number_of_nodes(), "nodes,", G.number_of_edges(), "edges")

if __name__ == "__main__":
    run()
