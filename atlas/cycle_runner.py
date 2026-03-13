import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import os
import re
from datetime import datetime
from pathlib import Path

from core.cycle_types import DayOfBrahmaConfig, CycleState


STOP = {
    "the","and","for","with","that","this","from","into","have","will","your","about",
    "atlas","system","knowledge","graph","layer","layers","using","used","been","they",
    "them","their","there","which","where","when","what","also","each","through","these",
    "those","than","then","were","would","could","should","being","many","more","most",
    "some","such","only","very","like","just","over","under","after","before","because",
    "while","across","within","between","around","make","made","does","doing","done",
    "ever","much","really","still","here","same","actually","already","project","repo",
    "file","files","data","ideas","concepts"
}


def slugify(s: str) -> str:
    s = s.strip().lower().replace(" ", "_")
    s = re.sub(r"[^a-z0-9_]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "untitled"


def iter_files(root: str):
    for base, _, files in os.walk(root):
        for name in files:
            if name.startswith("."):
                continue
            yield os.path.join(base, name)


def read_text(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def topic_candidates(text: str):
    words = re.findall(r"[A-Za-z][A-Za-z0-9_\-]{5,}", text.lower())
    freq = {}
    for w in words:
        if w in STOP or w.isdigit():
            continue
        freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return [w for w, _ in ranked[:8]]


def write_seed(seed_dir: str, topic: str, source_path: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"seed_{slugify(topic)}_{stamp}.md"
    out = os.path.join(seed_dir, name)
    body = f"""TITLE
{topic.title()}

ENTRY DOMAIN
Atlas Concept

TARGET DOMAIN
Knowledge Graph

ATTESTATION LEVEL
EXPERIMENTAL

LAYER PATH
concept
relation
visualization

SOURCE ENTITIES
{topic}

PROPOSED BRIDGE
Concept extracted from repository material and staged for graph ingestion.

WHY THIS MATTERS
Candidate research direction or structural concept for Atlas.

SOURCE FILE
{source_path}
"""
    Path(out).write_text(body, encoding="utf-8")
    return out


def seed_explosion(state: CycleState) -> None:
    os.makedirs(state.config.seed_dir, exist_ok=True)
    created = 0

    for root in state.config.source_dirs:
        if not os.path.exists(root):
            continue
        for path in iter_files(root):
            text = read_text(path)
            if not text.strip():
                continue
            for topic in topic_candidates(text)[:3]:
                write_seed(state.config.seed_dir, topic, path)
                created += 1

    state.counts["seeds_created"] = created
    state.add_result("seed_explosion", True, f"created {created} seeds")


def build_graph(state: CycleState) -> None:
    seed_dir = state.config.seed_dir
    nodes = {}
    links = []

    if not os.path.exists(seed_dir):
        os.makedirs(seed_dir, exist_ok=True)

    for fname in os.listdir(seed_dir):
        if not fname.endswith(".md"):
            continue
        path = os.path.join(seed_dir, fname)
        text = read_text(path)

        title_match = re.search(r"TITLE\s+(.+)", text)
        source_entities_match = re.search(r"SOURCE ENTITIES\s+(.+)", text)

        node_name = title_match.group(1).strip() if title_match else fname.replace(".md", "")
        node_id = slugify(node_name)

        if node_id not in nodes:
            nodes[node_id] = {"id": node_id, "type": "Concept", "source": path}

        if source_entities_match:
            parts = re.split(r"[,;]", source_entities_match.group(1))
            for p in parts:
                p = p.strip()
                if not p:
                    continue
                pid = slugify(p)
                if pid not in nodes:
                    nodes[pid] = {"id": pid, "type": "Concept", "source": path}
                links.append({
                    "source": node_id,
                    "target": pid,
                    "type": "associated_with"
                })

    graph = {"nodes": list(nodes.values()), "links": links}

    os.makedirs(os.path.dirname(state.config.graph_path), exist_ok=True)
    Path(state.config.graph_path).write_text(json.dumps(graph, indent=2), encoding="utf-8")
    Path(state.config.visual_graph_path).write_text(json.dumps(graph, indent=2), encoding="utf-8")

    state.counts["nodes"] = len(graph["nodes"])
    state.counts["edges"] = len(graph["links"])
    state.add_result("build_graph", True, f'nodes={len(graph["nodes"])} edges={len(graph["links"])}')


def render_mandala(state: CycleState) -> None:
    graph = json.loads(Path(state.config.visual_graph_path).read_text(encoding="utf-8"))
    nodes = graph.get("nodes", [])
    links = graph.get("links", [])

    width = 1400
    height = 1200
    cx = width // 2
    cy = height // 2
    rings = [120, 260, 420, 560]

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Atlas Mandala</title>
<style>
body {{
  margin: 0;
  background: black;
  color: white;
  font-family: sans-serif;
}}
#wrap {{
  padding: 16px;
}}
canvas {{
  background: black;
  display: block;
  margin: 0 auto;
  border: 1px solid #333;
}}
.info {{
  text-align: center;
  margin-bottom: 10px;
}}
</style>
</head>
<body>
<div id="wrap">
  <div class="info">
    <h2>Atlas Mandala</h2>
    <div>Nodes: {len(nodes)} | Edges: {len(links)}</div>
  </div>
  <canvas id="c" width="{width}" height="{height}"></canvas>
</div>
<script>
const nodes = {json.dumps(nodes)};
const links = {json.dumps(links)};
const canvas = document.getElementById("c");
const ctx = canvas.getContext("2d");
const cx = {cx};
const cy = {cy};
const rings = {json.dumps(rings)};

function ringFor(i) {{
  if (i < 12) return 0;
  if (i < 48) return 1;
  if (i < 120) return 2;
  return 3;
}}

function radiusFor(i) {{
  return rings[ringFor(i)];
}}

function countInRing(r) {{
  if (r === 0) return Math.min(12, nodes.length);
  if (r === 1) return Math.max(1, Math.min(36, nodes.length - 12));
  if (r === 2) return Math.max(1, Math.min(72, nodes.length - 48));
  return Math.max(1, nodes.length - 120);
}}

function offsetInRing(i) {{
  if (i < 12) return i;
  if (i < 48) return i - 12;
  if (i < 120) return i - 48;
  return i - 120;
}}

nodes.forEach((n, i) => {{
  const rix = ringFor(i);
  const radius = radiusFor(i);
  const count = countInRing(rix);
  const off = offsetInRing(i);
  const angle = (Math.PI * 2 * off / count) - Math.PI / 2;
  n.x = cx + Math.cos(angle) * radius;
  n.y = cy + Math.sin(angle) * radius;
}});

ctx.strokeStyle = "rgba(255,255,255,0.10)";
links.forEach(e => {{
  const a = nodes.find(n => n.id === e.source);
  const b = nodes.find(n => n.id === e.target);
  if (!a || !b) return;
  ctx.beginPath();
  ctx.moveTo(a.x, a.y);
  ctx.lineTo(b.x, b.y);
  ctx.stroke();
}});

nodes.forEach(n => {{
  let color = "white";
  if (n.type === "CosmicBody") color = "gold";
  if (n.type === "Cycle") color = "cyan";
  if (n.type === "Symbol") color = "violet";
  if (n.type === "Tool") color = "lime";

  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(n.x, n.y, 3.5, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "white";
  ctx.font = "11px sans-serif";
  ctx.fillText(n.id, n.x + 6, n.y + 4);
}});
</script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(state.config.mandala_path), exist_ok=True)
    Path(state.config.mandala_path).write_text(html, encoding="utf-8")
    state.add_result("render_mandala", True, state.config.mandala_path)


def write_cycle_report(state: CycleState) -> None:
    report = {
        "counts": state.counts,
        "results": [r.__dict__ for r in state.results]
    }
    Path("memory/visualizations/day_of_brahma_report.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )


def run_cycle() -> int:
    state = CycleState(config=DayOfBrahmaConfig())

    try:
        seed_explosion(state)
        build_graph(state)
        render_mandala(state)
        write_cycle_report(state)
    except Exception as e:
        state.add_result("cycle", False, str(e))
        write_cycle_report(state)
        print("Cycle failed:", e)
        return 1

    print("=== ATLAS CYCLE COMPLETE ===")
    for result in state.results:
        status = "OK" if result.ok else "FAIL"
        print(f"[{status}] {result.name}: {result.message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cycle())
