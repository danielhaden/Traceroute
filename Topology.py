import networkx as nx

class Topology:
    G = nx.null_graph()

    def __init__(self, gmlFilename=None):
        if gmlFilename != None:
            self.G.read_graphml(gmlFilename)

    def write_to_file(self, filename):
        nx.write_graphml(self.G, filename)

    def add_query(self, trace, verbose=False):
        antecedent = None
        for hop in trace.hops():
            currentVertex = hop[1]['ip']
            self.G.add_node(currentVertex)

            if antecedent != None:
                self.G.add_edge(antecedent, currentVertex)

            antecedent = currentVertex
