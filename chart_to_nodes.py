#!/usr/bin/env python3

import json
import sys

def nodes_from_chart(chart):

    nodes = []
    edges = []

    lagna = chart["lagna"]["rashi"]

    nodes.append(("Lagna", lagna))

    for planet,data in chart["planets"].items():

        nodes.append(("Planet", planet))

        edges.append((planet,"rashi",data["rashi"]))
        edges.append((planet,"nakshatra",data["nakshatra"]))
        edges.append((planet,"house",str(data["house_from_lagna"])))

    for step in chart["vimshottari_dasha"]:
        edges.append(("Moon","dasha",step["lord"]))

    return nodes,edges


def main():

    chart = json.load(sys.stdin)

    nodes,edges = nodes_from_chart(chart)

    print("\nATLAS NODES\n")

    for n in nodes:
        print("NODE",n[0],n[1])

    print("\nATLAS EDGES\n")

    for e in edges:
        print("EDGE",e[0],e[1],e[2])


if __name__ == "__main__":
    main()
