#!/usr/bin/env python3

import json
import subprocess
import sys
from datetime import datetime

GRAPH_FILE = "memory/graphs/atlas_graph.json"

def canonical(name):
    return name.lower().replace(" ", "_")

def load_graph():
    try:
        with open(GRAPH_FILE) as f:
            return json.load(f)
    except:
        return {"nodes": [], "edges": []}

def save_graph(graph):
    with open(GRAPH_FILE, "w") as f:
        json.dump(graph, f, indent=2)

def add_node(graph, node):
    if node["id"] not in [n["id"] for n in graph["nodes"]]:
        graph["nodes"].append(node)

def add_edge(graph, source, rel, target):
    graph["edges"].append({
        "from": source,
        "relation": rel,
        "to": target
    })

def run_engine(args):

    raw = subprocess.check_output(
        ["python", "/opt/atlas/astro_block.py"] + args
    )

    return json.loads(raw)

def build_graph(chart, args):

    year,month,day,hour,lat,lon = args

    chart_id = f"chart.user_{year}"

    graph = load_graph()

    chart_node = {
        "id": chart_id,
        "type": "chart",
        "timestamp": f"{year}-{month}-{day}T{hour}",
        "lat": float(lat),
        "lon": float(lon)
    }

    add_node(graph, chart_node)

    for graha,data in chart["planets"].items():

        g = canonical(graha)

        placement_id = f"placement.user_{year}.{g}"

        placement = {
            "id": placement_id,
            "type": "placement",
            "graha": g,
            "longitude": data["longitude"]
        }

        add_node(graph, placement)

        add_edge(graph, chart_id, "has_placement", placement_id)

        add_edge(graph, placement_id, "is", f"entity.{g}")

        r = canonical(data["rashi"])
        add_edge(graph, placement_id, "in_rashi", f"rashi.{r}")

        n = canonical(data["nakshatra"])
        add_edge(graph, placement_id, "in_nakshatra", f"nakshatra.{n}")

        p = data["pada"]
        add_edge(graph, placement_id, "in_pada", f"pada.{n}_{p}")

        h = data["house_from_lagna"]
        add_edge(graph, placement_id, "in_house", f"house.{h}")

        nav = canonical(data["navamsa_sign"])
        add_edge(graph, placement_id, "in_navamsa", f"rashi.{nav}")

    save_graph(graph)

    print("Atlas graph updated")
    print("chart:", chart_id)

def main():

    args = sys.argv[1:]

    chart = run_engine(args)

    build_graph(chart, args)

if __name__ == "__main__":
    main()
