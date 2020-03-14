import networkx as nx

class Topology:
    G = nx.null_graph()

    def __init__(self, gmlFilename=None):
        if gmlFilename != None:
            self.G.read_graphml(gmlFilename)

    def write_to_file(self, filename):
        nx.write_graphml(self.G, filename)

    def add_query(self, query, verbose=False):

        for index in query.get_trace_indices():

            antecedent = None
            for hop, ip, name, time in query.items(index):

                if ip!='*':
                    self.G.add_node(ip, name=name, t1=time[0], t2=time[1], t3=time[2])
                    if verbose:
                        print("Added node", ip)

                    if antecedent != None: ## add edge if previous node was connected
                        self.G.add_edge(antecedent, ip)
                        if verbose:
                            print("Added link between", antecedent, "and", ip)

                    antecedent = ip

                else:
                    antecedent = None