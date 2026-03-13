import json, sqlite3, csv, time
from pathlib import Path

BASE = Path("/opt/atlas")
REPORTS = BASE/"memory"/"reports"
REPORTS.mkdir(parents=True, exist_ok=True)

DASH = REPORTS/"dashboard.html"
GAPS = REPORTS/"gaps_top.txt"
AGG  = REPORTS/"aggregate.json"
SEED_GRAPH = BASE/"memory"/"graphs"/"seed_graph.json"

DB = BASE/"memory"/"corpus.db"

def read_text(p: Path, default=""):
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else default

def graph_stats(p: Path):
    if not p.exists(): return (0,0)
    d = json.loads(p.read_text(encoding="utf-8"))
    return (len(d.get("nodes",[])), len(d.get("links",[])))

def corpus_stats():
    if not DB.exists():
        return {"db":"missing"}
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM files")
    files = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passages")
    passages = cur.fetchone()[0]
    cur.execute("SELECT status, COUNT(*) FROM staged_relations GROUP BY status")
    staged = dict(cur.fetchall())
    con.close()
    return {"files": files, "passages": passages, "staged": staged}

def factcheck_summary():
    # reuse existing atlas factcheck output if available by reading csv directly
    rels = [
        BASE/"datasets"/"relations_nakshatra_deity.csv",
        BASE/"datasets"/"relations_devi_weapon.csv",
        BASE/"datasets"/"relations_nakshatra_plants.csv",
    ]
    miss_to=0
    miss_ev=0
    total=0
    for p in rels:
        if not p.exists(): continue
        with p.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                total += 1
                if not (r.get("to_id") or "").strip():
                    miss_to += 1
                ev_ok = all((r.get(k) or "").strip() for k in ["source_title","source_locator","excerpt"])
                if not ev_ok:
                    miss_ev += 1
    return {"total": total, "missing_to": miss_to, "missing_ev": miss_ev}

def main():
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    gaps = read_text(GAPS, "(run: atlas gaps)")
    agg = {}
    if AGG.exists():
        try: agg = json.loads(AGG.read_text(encoding="utf-8"))
        except Exception: agg = {}
    gnodes, glinks = graph_stats(SEED_GRAPH)
    corpus = corpus_stats()
    fc = factcheck_summary()

    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Atlas Dashboard</title>
  <style>
    body {{ font-family: sans-serif; background:#111; color:#eee; margin:20px; }}
    .card {{ background:#1e1e1e; padding:16px; border-radius:12px; margin-bottom:16px; }}
    pre {{ background:#0f0f0f; padding:12px; border-radius:10px; overflow:auto; }}
    a {{ color:#7dd3fc; }}
    .row {{ display:flex; gap:16px; flex-wrap:wrap; }}
    .kpi {{ font-size:20px; }}
  </style>
</head>
<body>
<h1>Atlas Dashboard</h1>
<div class="card">Generated: {now}</div>

<div class="row">
  <div class="card" style="flex:1;min-width:280px">
    <div class="kpi">Seed Graph</div>
    <div>nodes: <b>{gnodes}</b> &nbsp; links: <b>{glinks}</b></div>
    <div style="margin-top:10px">Open graph via CLI:</div>
    <pre>atlas seedgraph
atlas graph seed</pre>
  </div>

  <div class="card" style="flex:1;min-width:280px">
    <div class="kpi">Factcheck</div>
    <div>total rows: <b>{fc['total']}</b></div>
    <div>missing to_id: <b>{fc['missing_to']}</b></div>
    <div>missing evidence: <b>{fc['missing_ev']}</b></div>
    <pre>atlas factcheck</pre>
  </div>

  <div class="card" style="flex:1;min-width:280px">
    <div class="kpi">Corpus</div>
    <div>files: <b>{corpus.get('files','-')}</b> &nbsp; passages: <b>{corpus.get('passages','-')}</b></div>
    <div>staged: <b>{corpus.get('staged',{})}</b></div>
    <pre>atlas corpus_scan
atlas corpus_pdftext
atlas corpus_harvest
atlas stage 50
atlas adopt 50</pre>
  </div>
</div>

<div class="card">
  <div class="kpi">Top Gaps (what to improve next)</div>
  <pre>{gaps}</pre>
  <pre>atlas gaps
atlas pick</pre>
</div>

<div class="card">
  <div class="kpi">Aggregate Report</div>
  <pre>{json.dumps(agg, indent=2) if agg else "(run: atlas aggregate)"}</pre>
</div>

<div class="card">
  <div class="kpi">Safe Update</div>
  <pre>atlas test
DO_PULL=1 atlas safeupdate</pre>
</div>

</body>
</html>"""

    DASH.write_text(html, encoding="utf-8")
    print("Wrote:", DASH)

if __name__ == "__main__":
    main()
