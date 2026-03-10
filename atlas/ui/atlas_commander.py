import curses
import math
from collections import Counter

from atlas.core.graph_store import edge_type, load_graph, node_label

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "PurvaPhalguni",
    "UttaraPhalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "PurvaAshadha", "UttaraAshadha",
    "Shravana", "Dhanishta", "Shatabhisha", "PurvaBhadra",
    "UttaraBhadra", "Revati",
]

MENU = [
    ("Sanctum", "Atlas readiness + coherence snapshot"),
    ("Stats", "Graph metrics + relation signatures"),
    ("Mandala", "Radial projection from graph nodes"),
    ("Nakshatra", "27-fold lunar wheel"),
    ("Nodes", "Scrollable node browser"),
    ("Quit", "Exit"),
]


def safe_addstr(stdscr, y, x, text, attr=0):
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h or x >= w:
        return
    text = str(text)
    if x < 0:
        text = text[-x:]
        x = 0
    if not text:
        return
    text = text[: max(0, w - x - 1)]
    if not text:
        return
    try:
        stdscr.addstr(y, x, text, attr)
    except curses.error:
        pass


def graph_metrics(graph):
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    node_count = len(nodes)
    edge_count = len(edges)
    density = (edge_count / node_count) if node_count else 0.0
    avg_degree = (2 * edge_count / node_count) if node_count else 0.0

    node_types = Counter(
        str(n.get("type") or n.get("kind") or "unknown") for n in nodes
    )
    relations = Counter(edge_type(e) for e in edges)

    return {
        "source": graph.get("_source") or "none",
        "nodes": node_count,
        "edges": edge_count,
        "density": density,
        "avg_degree": avg_degree,
        "top_node_types": node_types.most_common(6),
        "top_relations": relations.most_common(6),
    }


def draw_header(stdscr, title, subtitle=""):
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, 0, 2, title, curses.A_BOLD)
    if subtitle:
        safe_addstr(stdscr, 1, 2, subtitle)
    safe_addstr(stdscr, 2, 0, "-" * max(1, w - 1))


def draw_footer(stdscr, text):
    h, w = stdscr.getmaxyx()
    safe_addstr(stdscr, h - 2, 0, "-" * max(1, w - 1))
    safe_addstr(stdscr, h - 1, 2, text)


def show_sanctum(stdscr):
    stdscr.clear()
    graph = load_graph()
    metrics = graph_metrics(graph)
    draw_header(stdscr, "ATLAS SANCTUM", "Front gate for a living relational graph")

    lines = [
        f"Source: {metrics['source']}",
        f"Nodes: {metrics['nodes']}   Edges: {metrics['edges']}   Edges/Node: {metrics['density']:.2f}",
        f"Avg degree: {metrics['avg_degree']:.2f}",
        "",
        "Readiness pulse:",
        f"  {'OK' if metrics['nodes'] > 0 else 'WAIT'} graph has nodes",
        f"  {'OK' if metrics['edges'] > 0 else 'WAIT'} graph has relations",
        f"  {'OK' if metrics['density'] >= 1.0 else 'GROW'} relation density moving toward 1.0+",
        "",
        "This interface is projection-only. Graph remains truth layer.",
    ]

    y = 4
    for line in lines:
        safe_addstr(stdscr, y, 4, line)
        y += 1

    draw_footer(stdscr, "Enter: open selected view    q: back")
    stdscr.refresh()
    stdscr.getch()


def show_stats(stdscr):
    stdscr.clear()
    graph = load_graph()
    metrics = graph_metrics(graph)

    draw_header(stdscr, "GRAPH STATS", "Measured from active graph source")
    safe_addstr(stdscr, 4, 4, f"Source: {metrics['source']}")
    safe_addstr(stdscr, 5, 4, f"Node count: {metrics['nodes']}")
    safe_addstr(stdscr, 6, 4, f"Edge count: {metrics['edges']}")
    safe_addstr(stdscr, 7, 4, f"Edges per node: {metrics['density']:.2f}")
    safe_addstr(stdscr, 8, 4, f"Average degree: {metrics['avg_degree']:.2f}")

    y = 10
    safe_addstr(stdscr, y, 4, "Top node types:", curses.A_BOLD)
    y += 1
    for t, count in metrics["top_node_types"]:
        safe_addstr(stdscr, y, 6, f"- {t}: {count}")
        y += 1

    y += 1
    safe_addstr(stdscr, y, 4, "Top relation types:", curses.A_BOLD)
    y += 1
    for rel, count in metrics["top_relations"]:
        safe_addstr(stdscr, y, 6, f"- {rel}: {count}")
        y += 1

    draw_footer(stdscr, "Press any key to return")
    stdscr.refresh()
    stdscr.getch()


def radial_points(labels, radius):
    if not labels:
        return []
    out = []
    total = len(labels)
    for i, label in enumerate(labels):
        angle = (2 * math.pi * i / total) - (math.pi / 2)
        x = int(math.cos(angle) * radius)
        y = int(math.sin(angle) * radius * 0.5)
        out.append((label, x, y))
    return out


def show_mandala(stdscr):
    stdscr.clear()
    graph = load_graph()
    labels = [node_label(n) for n in graph.get("nodes", [])[:36]]
    h, w = stdscr.getmaxyx()
    cx = w // 2
    cy = h // 2
    radius = max(6, min(w // 4, max(6, h // 3)))
    draw_header(stdscr, "MANDALA VIEW", "First 36 nodes in radial projection")
    safe_addstr(stdscr, cy, cx, "O", curses.A_BOLD)
    for label, dx, dy in radial_points(labels, radius):
        safe_addstr(stdscr, cy + dy, cx + dx, "*")
        safe_addstr(stdscr, cy + dy, cx + dx + 2, label[:10])
    draw_footer(stdscr, "Press any key to return")
    stdscr.refresh()
    stdscr.getch()


def show_nakshatra(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    cx = w // 2
    cy = h // 2
    radius = max(8, min(w // 4, max(8, h // 3)))
    draw_header(stdscr, "NAKSHATRA WHEEL", "27 lunar mansions")
    safe_addstr(stdscr, cy, cx, "O", curses.A_BOLD)
    for label, dx, dy in radial_points(NAKSHATRAS, radius):
        safe_addstr(stdscr, cy + dy, cx + dx, "*")
        safe_addstr(stdscr, cy + dy, cx + dx + 2, label[:10])
    draw_footer(stdscr, "Press any key to return")
    stdscr.refresh()
    stdscr.getch()


def show_nodes(stdscr):
    graph = load_graph()
    labels = [node_label(n) for n in graph.get("nodes", [])]
    if not labels:
        labels = ["No nodes found."]
    pos = 0
    while True:
        stdscr.clear()
        h, _ = stdscr.getmaxyx()
        draw_header(stdscr, "NODE BROWSER", f"Total nodes: {len(labels)}")
        page = max(1, h - 6)
        visible = labels[pos:pos + page]
        y = 4
        for idx, label in enumerate(visible, start=pos + 1):
            safe_addstr(stdscr, y, 4, f"{idx:>4}. {label}")
            y += 1
        draw_footer(stdscr, "Up/Down or j/k scroll   q return")
        stdscr.refresh()
        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            return
        if key in (curses.KEY_DOWN, ord("j")) and pos + page < len(labels):
            pos += 1
        elif key in (curses.KEY_UP, ord("k")) and pos > 0:
            pos -= 1


def dispatch(stdscr, name):
    if name == "Sanctum":
        show_sanctum(stdscr)
    elif name == "Stats":
        show_stats(stdscr)
    elif name == "Mandala":
        show_mandala(stdscr)
    elif name == "Nakshatra":
        show_nakshatra(stdscr)
    elif name == "Nodes":
        show_nodes(stdscr)


def draw_menu(stdscr, selected):
    stdscr.clear()
    draw_header(stdscr, "ATLAS COMMANDER", "Select a projection")
    y = 5
    for i, (name, desc) in enumerate(MENU):
        attr = curses.A_REVERSE if i == selected else 0
        safe_addstr(stdscr, y, 6, f"{name:<10}  {desc}", attr)
        y += 1
    draw_footer(stdscr, "Up/Down move   Enter select   q quit")
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    selected = 0
    while True:
        draw_menu(stdscr, selected)
        key = stdscr.getch()
        if key in (ord("q"), ord("Q")):
            break
        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % len(MENU)
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % len(MENU)
        elif key in (10, 13):
            name = MENU[selected][0]
            if name == "Quit":
                break
            dispatch(stdscr, name)


if __name__ == "__main__":
    curses.wrapper(main)
