import json, sys, time, webbrowser
from pathlib import Path
import networkx as nx
from pyvis.network import Network

BASE = Path("/opt/atlas")
DEFAULTS = {
    "seed": BASE / "memory" / "graphs" / "seed_graph.json",
    "vedic": BASE / "memory" / "vedic_cosmology_graph.json",
    "canonical": BASE / "memory" / "graphs" / "canonical_graph.json",
    "concepts": BASE / "memory" / "concepts.json",
}

def load_graph(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing graph file: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if "nodes" in data and "links" in data:
        G = nx.Graph()
        for n in data["nodes"]:
            G.add_node(n.get("id"), **n)
        for e in data["links"]:
            G.add_edge(e.get("source"), e.get("target"), **e)
        return G
    return nx.node_link_graph(data)

def node_id_type(node_id: str) -> str:
    return node_id.split(":", 1)[0] if ":" in node_id else "unknown"

# Map raw types to semantic layers you care about
TYPE_TO_LAYER = {
    "nakshatra": "Nakshatra",
    "tithi": "Tithi",
    "nitya_devi": "Deity/Devi",
    "deity": "Deity/Devi",
    "devi": "Deity/Devi",
    "graha": "Graha",
    "rashi": "Rashi",
    "plant": "Plants",
    "raga": "Music",
    "tala": "Music",
    "instrument": "Music",
    "ritual": "Ritual",
    "festival": "Ritual",
    "todo": "TODO",
    "concept": "Concepts",
    "text": "Texts",
    "source": "Texts",
    "passage": "Texts",
    "weapon": "Iconography",
    "symbol": "Iconography",
}

def layer_for(node_id: str) -> str:
    t = node_id_type(node_id)
    return TYPE_TO_LAYER.get(t, "Other")

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "seed"
    if mode not in DEFAULTS:
        print("Usage: atlas graph [seed|vedic|canonical|concepts]")
        return

    G = load_graph(DEFAULTS[mode])
    out = BASE / "memory" / f"graph_{mode}_{int(time.time())}.html"

    net = Network(height="900px", width="100%", bgcolor="#111", font_color="white")
    net.toggle_physics(True)

    # Add nodes with a semantic layer label (stored in group)
    for node, attrs in G.nodes(data=True):
        lid = layer_for(str(node))
        net.add_node(node, label=str(node), group=lid)

    for a, b, attrs in G.edges(data=True):
        net.add_edge(a, b, title=str(attrs.get("relation","")))

    # Basic buttons still useful
    net.show_buttons(filter_=["physics"])

    # Inject JS for:
    # - Layer toggles (show/hide by group)
    # - Focus mode (BFS radius from node)
    # - Reset view
    custom_js = r"""
<script type="text/javascript">
(function() {

  // --- helpers ---
  function uniq(arr) { return Array.from(new Set(arr)); }
  function allGroups() {
    var all = nodes.get();
    return uniq(all.map(n => n.group || "Other")).sort();
  }

  function setVisibilityByGroups(enabledGroups) {
    var enabled = new Set(enabledGroups);
    var all = nodes.get();
    for (var i=0;i<all.length;i++){
      var n = all[i];
      var show = enabled.has(n.group || "Other");
      nodes.update({id: n.id, hidden: !show});
    }
    // edges auto-hide if either endpoint hidden (vis handles that)
  }

  // Build adjacency for focus (from current edges)
  function buildAdj() {
    var adj = {};
    var allIds = nodes.getIds();
    allIds.forEach(id => adj[id] = []);
    edges.get().forEach(e => {
      if (!(e.from in adj)) adj[e.from] = [];
      if (!(e.to in adj)) adj[e.to] = [];
      adj[e.from].push(e.to);
      adj[e.to].push(e.from);
    });
    return adj;
  }

  function findNodeByQuery(q) {
    q = (q||"").trim().toLowerCase();
    if (!q) return null;

    // exact id match
    var ids = nodes.getIds();
    for (var i=0;i<ids.length;i++){
      if (String(ids[i]).toLowerCase() === q) return ids[i];
    }

    // contains match on id label
    for (var i=0;i<ids.length;i++){
      if (String(ids[i]).toLowerCase().includes(q)) return ids[i];
    }
    return null;
  }

  function focusNeighborhood(rootId, radius) {
    var adj = buildAdj();
    var seen = new Set([rootId]);
    var frontier = [rootId];

    for (var d=0; d<radius; d++){
      var next = [];
      frontier.forEach(u => {
        (adj[u] || []).forEach(v => {
          if (!seen.has(v)) {
            seen.add(v);
            next.push(v);
          }
        });
      });
      frontier = next;
      if (frontier.length === 0) break;
    }

    // hide everything not in seen
    var all = nodes.getIds();
    for (var i=0;i<all.length;i++){
      var id = all[i];
      nodes.update({id: id, hidden: !seen.has(id)});
    }

    // bring focus into view
    try {
      network.selectNodes([rootId]);
      network.focus(rootId, {scale: 1.2, animation: true});
    } catch(e) {}
  }

  function resetAll() {
    // show all nodes
    var all = nodes.getIds();
    for (var i=0;i<all.length;i++){
      nodes.update({id: all[i], hidden: false});
    }
    try { network.fit({animation: true}); } catch(e) {}
  }

  // --- UI ---
  var container = document.getElementById("mynetwork");
  var panel = document.createElement("div");
  panel.style.padding = "10px";
  panel.style.fontFamily = "sans-serif";
  panel.style.color = "white";
  panel.style.background = "#222";
  panel.style.borderRadius = "8px";
  panel.style.marginBottom = "8px";

  var groups = allGroups();

  // Build layer toggles
  var html = `<div style="display:flex;gap:18px;flex-wrap:wrap;align-items:center">
    <div><b>Layers</b> (toggle)</div>
    <div id="layerToggles" style="display:flex;gap:12px;flex-wrap:wrap"></div>
  </div>
  <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;align-items:center">
    <div><b>Focus</b> (neighborhood)</div>
    <input id="focusQuery" placeholder="rohini or nakshatra:4" style="padding:6px;border-radius:6px;border:1px solid #444;background:#111;color:#fff;min-width:240px" />
    <label>Radius
      <select id="focusRadius" style="padding:6px;border-radius:6px;border:1px solid #444;background:#111;color:#fff">
        <option value="1">1 hop</option>
        <option value="2" selected>2 hops</option>
        <option value="3">3 hops</option>
      </select>
    </label>
    <button id="btnFocus">Focus</button>
    <button id="btnReset">Reset</button>
    <span style="opacity:0.8">Tip: focus "rohini" to view its local cluster.</span>
  </div>`;

  panel.innerHTML = html;
  container.parentNode.insertBefore(panel, container);

  var togglesDiv = document.getElementById("layerToggles");

  // Default: show all layers
  var enabledGroups = new Set(groups);

  groups.forEach(g => {
    var id = "cb_" + g.replace(/[^a-z0-9]/gi, "_");
    var wrap = document.createElement("label");
    wrap.style.display = "inline-flex";
    wrap.style.alignItems = "center";
    wrap.style.gap = "6px";
    wrap.innerHTML = `<input type="checkbox" id="${id}" checked /> <span>${g}</span>`;
    togglesDiv.appendChild(wrap);

    document.getElementById(id).addEventListener("change", (ev) => {
      if (ev.target.checked) enabledGroups.add(g);
      else enabledGroups.delete(g);
      setVisibilityByGroups(Array.from(enabledGroups));
    });
  });

  document.getElementById("btnReset").onclick = function() {
    // check all boxes + show all
    enabledGroups = new Set(groups);
    groups.forEach(g => {
      var id = "cb_" + g.replace(/[^a-z0-9]/gi, "_");
      document.getElementById(id).checked = true;
    });
    resetAll();
  };

  document.getElementById("btnFocus").onclick = function() {
    var q = document.getElementById("focusQuery").value;
    var r = parseInt(document.getElementById("focusRadius").value || "2", 10);
    var node = findNodeByQuery(q);
    if (!node) {
      alert("No matching node found for: " + q);
      return;
    }
    focusNeighborhood(node, r);
  };

})();
</script>
"""
    net.html = net.html.replace("</body>", custom_js + "\n</body>")

    net.write_html(str(out))
    print("Graph written to:", out)
    webbrowser.open("file://" + str(out))

if __name__ == "__main__":
    main()
