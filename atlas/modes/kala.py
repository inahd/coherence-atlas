def run(graph):

    print("\nKala Explorer\n")

    for n,d in graph.nodes.items():

        if d.get("domain") == "kala":
            print("-", d.get("name"))
