class Graph:

    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, data):
        self.nodes[node_id] = data

    def add_edge(self, a, r, b):
        self.edges.append((a, r, b))

    def neighbors(self, node):
        return [e for e in self.edges if e[0] == node or e[2] == node]
