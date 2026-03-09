from atlas.core.graph_store import load_graph, node_label

def research_prompts():
    g = load_graph()
    labels = [node_label(n) for n in g.get("nodes", [])]

    prompts = []

    if len(labels) >= 2:
        prompts.append(f"Which conceptual patterns connect {labels[0]} and {labels[-1]}?")

    prompts.append("Which nodes share symbolic correspondences?")
    prompts.append("Which nodes could form a new mandala cluster?")
    prompts.append("What cosmological layer does this pattern belong to?")

    return prompts

def expansion_prompts():
    return [
        "Add deity correspondences",
        "Add elemental associations",
        "Add mantra frequencies",
        "Add mythological references",
        "Add botanical correspondences",
    ]
