from flask import Flask, jsonify, request
from pathlib import Path
import subprocess, yaml
from collections import Counter

BASE = Path("/opt/atlas")
DATASETS = BASE / "datasets"

app = Flask(__name__)

def run(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {"cmd": cmd, "code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}

def walk(x, c):
    if isinstance(x, dict):
        for k,v in x.items():
            c[k]+=1
            walk(v,c)
    elif isinstance(x, list):
        for i in x:
            walk(i,c)

@app.get("/ping")
def ping():
    return jsonify({"ok": True})

@app.get("/keys")
def keys():
    files = request.args.get("files", "nakshatra.yaml,deities.yaml,jyotish_core.yaml").split(",")
    out = {}
    for f in files:
        p = DATASETS / f
        if not p.exists():
            out[f] = {"missing": True}
            continue
        data = yaml.safe_load(p.read_text(encoding="utf-8", errors="ignore"))
        c = Counter(); walk(data, c)
        out[f] = {"top_keys": c.most_common(30)}
    return jsonify(out)

# --- allow both GET and POST for convenience ---
@app.route("/autolink", methods=["GET","POST"])
def autolink():
    return jsonify(run("atlas autolink"))

@app.route("/factcheck", methods=["GET","POST"])
def factcheck():
    return jsonify(run("atlas factcheck"))

@app.route("/seedgraph", methods=["GET","POST"])
def seedgraph():
    return jsonify(run("atlas seedgraph"))

@app.get("/files")
def files():
    root = request.args.get("root","/opt/atlas/datasets")
    p = Path(root)
    if not p.exists():
        return jsonify({"error":"missing", "root":root}), 404
    items = [{"name": x.name, "is_dir": x.is_dir()} for x in sorted(p.glob("*"))]
    return jsonify({"root": root, "items": items})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7077)
