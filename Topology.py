import networkx as nx
from Trace import *

class Topology:
    G = nx.null_graph()

    def add_probe(self, trace):
        for key in trace:
            self.G.add_node(key)

