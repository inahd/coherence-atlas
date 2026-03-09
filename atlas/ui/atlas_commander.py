import curses
import math
from atlas.core.graph_store import load_graph, node_label, edge_type

NAKSHATRAS = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra",
    "Punarvasu","Pushya","Ashlesha","Magha","PurvaPhalguni",
    "UttaraPhalguni","Hasta","Chitra","Swati","Vishakha",
    "Anuradha","Jyeshtha","Mula","PurvaAshadha","UttaraAshadha",
    "Shravana","Dhanishta","Shatabhisha","PurvaBhadra",
    "UttaraBhadra","Revati"
]

MENU = [
    ("Home", "Atlas overview"),
    ("Stats", "Graph statistics"),
    ("Mandala", "Radial node map"),
    ("Nakshatra", "27-fold wheel"),
    ("Nodes", "Browse node labels"),
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

def show_home(stdscr):
    stdscr.clear()
    graph = load_graph()
    draw_header(stdscr, "ATLAS COMMANDER", "Cosmic terminal interface")
    lines = [
        f"Graph source: {graph.get('_source')}",
        f"Nodes: {len(graph['nodes'])}",
        f"Edges: {len(graph['edges'])}",
        "",
        "Views:",
        "  Stats      graph counts and sample data",
        "  Mandala    radial projection of nodes",
        "  Nakshatra  27-fold wheel",
        "  Nodes      scrollable node list",
    ]
    y = 4
    for line in lines:
        safe_addstr(stdscr, y, 4, line)
        y += 1
    draw_footer(stdscr, "Press any key to return")
    stdscr.refresh()
    stdscr.getch()

def show_stats(stdscr):
    stdscr.clear()
    graph = load_graph()
    draw_header(stdscr, "GRAPH STATS")
    safe_addstr(stdscr, 4, 4, f"Source: {graph.get('_source')}")
    safe_addstr(stdscr, 5, 4, f"Node count: {len(graph['nodes'])}")
    safe_addstr(stdscr, 6, 4, f"Edge count: {len(graph['edges'])}")

    y = 8
    safe_addstr(stdscr, y, 4, "First 8 nodes:")
    y += 1
    for node in graph["nodes"][:8]:
        safe_addstr(stdscr, y, 6, f"- {node_label(node)}")
        y += 1

    safe_addstr(stdscr, y + 1, 4, "First 8 edges:")
    y += 2
    for edge in graph["edges"][:8]:
        src = edge.get("source", "?")
        dst = edge.get("target", "?")
        rel = edge_type(edge)
        safe_addstr(stdscr, y, 6, f"- {src} --{rel}--> {dst}")
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
    labels = [node_label(n) for n in graph["nodes"][:36]]
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
    labels = [node_label(n) for n in graph["nodes"]]
    if not labels:
        labels = ["No nodes found."]
    pos = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        draw_header(stdscr, "NODE BROWSER", f"Total nodes: {len(labels)}")
        page = max(1, h - 6)
        visible = labels[pos:pos + page]
        y = 4
        for idx, label in enumerate(visible, start=pos + 1):
            safe_addstr(stdscr, y, 4, f"{idx:>4}. {label}")
            y += 1
        draw_footer(stdscr, "Up/Down scroll   q return")
        stdscr.refresh()
        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            return
        if key == curses.KEY_DOWN and pos + page < len(labels):
            pos += 1
        elif key == curses.KEY_UP and pos > 0:
            pos -= 1

def dispatch(stdscr, name):
    if name == "Home":
        show_home(stdscr)
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
        if key == curses.KEY_UP:
            selected = (selected - 1) % len(MENU)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(MENU)
        elif key in (10, 13):
            name = MENU[selected][0]
            if name == "Quit":
                break
            dispatch(stdscr, name)

if __name__ == "__main__":
    curses.wrapper(main)
