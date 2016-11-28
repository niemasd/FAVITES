#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetwork" module, implemented with NetworkX
'''
from ContactNetwork import ContactNetwork # abstract ContactNetwork class
import networkx as nx                     # using NetworkX to implement
from ContactNetworkNode_NetworkX import ContactNetworkNode_NetworkX as Node # Node class

class ContactNetwork_NetworkX(ContactNetwork):
    '''
    Implement the ``ContactNetwork`` abstract class using NetworkX

    Attributes
    ----------
    contact_network : Graph
        The NetworkX ``Graph'' object to represent this ``ContactNetwork''
    infected_nodes : set of ContactNetworkNode
        Set containing the nodes that have been infected
    name_to_num : dict
        Dictionary mapping original node names to numbers
    num_to_name : dict
        Dictionary mapping numbers to original node names
    transmissions : list
        List of transmission events as (u,v,time) tuples
    '''
    def __init__(self, edge_list):
        # set up NetworkX and graph
        self.contact_network = nx.Graph()
        self.name_to_num = {}       # map original node names to numbers
        self.num_to_name = []       # map numbers to original node names
        self.infected_nodes = set() # store numbers of infected nodes
        self.transmissions = []     # store u->v transmission as (u,v,time)

        # read in Contact Network as edge list
        for line in edge_list:
            u,v = line.split('\t') # TODO: PARSE u AND v FOR NODE ATTRIBUTES (e.g. MSM, etc.)
            if u not in self.name_to_num:
                self.contact_network.add_node(len(self.num_to_name))
                self.name_to_num[u] = len(self.num_to_name)
                self.num_to_name.append(u)
            if v not in self.name_to_num:
                self.contact_network.add_node(len(self.num_to_name))
                self.name_to_num[v] = len(self.num_to_name)
                self.num_to_name.append(v)
            self.contact_network.add_edge(self.name_to_num[u],
                self.name_to_num[v])

    def num_transmissions(self):
        return len(self.transmissions)

    def num_nodes(self):
        return self.contact_network.number_of_nodes()

    def num_infected_nodes(self):
        return len(self.infected_nodes)

    def num_uninfected_nodes(self):
        return self.contact_network.number_of_nodes()-self.num_infected_nodes()

    def num_edges(self):
        return self.contact_network.number_of_edges()

    def nodes_iter(self):
        for node in self.contact_network.nodes():
            yield Node(self.contact_network, self.num_to_name[node])

    def edges_iter(self):
        return self.contact_network.edges()

    def get_transmissions(self):
        return self.transmissions

def check():
    '''
    Check ``ContactNetwork_NetworkX`` for validity
    '''
    print("--- Testing ContactNetwork_NetworkX Module ---")
    print("Instantiation: ",end='')
    g = ContactNetwork_NetworkX(['A\tB','A\tC','B\tC','A\tD','C\tD'])
    status = "Success"
    if not isinstance(g, ContactNetwork):
        status = "Failure"
    elif g.num_nodes() != 4:
        status = "Failure"
    elif g.num_edges() != 5:
        status = "Failure"
    print(status)

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    check()