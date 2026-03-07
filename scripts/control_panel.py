from flask import Flask
import subprocess
import os

app = Flask(__name__)

ROOT="/opt/atlas"

def run(cmd):
    return subprocess.getoutput(cmd)

@app.route("/")
def home():

    cpu = run("top -bn1 | grep 'Cpu(s)'")
    mem = run("free -h | grep Mem")
    git = run("git status -sb 2>/dev/null")
    models = run("ollama list")

    return f"""
<html>
<head>
<title>Atlas AI Control Center</title>
<style>
body {{ background:#111;color:#eee;font-family:Arial;padding:30px }}
h1 {{ color:#6cf }}
.box {{ margin-bottom:30px }}
pre {{ background:#222;padding:10px }}
a {{ color:#9f9 }}
</style>
</head>
<body>

<h1>Atlas AI Control Center</h1>

<div class="box">
<h2>System</h2>
<pre>{cpu}
{mem}</pre>
</div>

<div class="box">
<h2>Git</h2>
<pre>{git}</pre>
<a href="/git_pull">Pull</a> |
<a href="/git_push">Push</a>
</div>

<div class="box">
<h2>Ollama</h2>
<pre>{models}</pre>
<a href="/start_ollama">Start Ollama</a>
</div>

<div class="box">
<h2>AI Tools</h2>
<a href="/run_shell">Launch AI Dev Shell</a><br>
<a href="/build_index">Rebuild Project Index</a><br>
<a href="/build_vectors">Rebuild Vector Memory</a>
</div>

</body>
</html>
"""

@app.route("/start_ollama")
def start_ollama():
    return "<pre>"+run("ollama serve &")+"</pre>"

@app.route("/git_pull")
def git_pull():
    return "<pre>"+run("git pull")+"</pre>"

@app.route("/git_push")
def git_push():
    return "<pre>"+run("git add . && git commit -m 'dashboard update' && git push")+"</pre>"

@app.route("/run_shell")
def run_shell():
    os.system("gnome-terminal -- bash -c 'cd /opt/atlas && source venv/bin/activate && python scripts/dev_ai_shell.py'")
    return "AI shell launched."

@app.route("/build_index")
def build_index():
    return "<pre>"+run("python scripts/index_project.py")+"</pre>"

@app.route("/build_vectors")
def build_vectors():
    return "<pre>"+run("python scripts/vector_memory.py")+"</pre>"

app.run(port=7010)
