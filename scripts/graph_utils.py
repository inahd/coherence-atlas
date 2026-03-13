def add_node(nodes,name,data):
    if name not in nodes:
        nodes[name]=data

def add_edge(edges,a,rel,b):
    edge={"from":a,"relation":rel,"to":b}
    if edge not in edges:
        edges.append(edge)
