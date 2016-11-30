#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetwork" module, implemented with NetworkX
'''
from ContactNetwork import ContactNetwork # abstract ContactNetwork class
from networkx import DiGraph              # using NetworkX to implement
from ContactNetworkNode_NetworkX import ContactNetworkNode_NetworkX as Node # Node class
from ContactNetworkEdge_NetworkX import ContactNetworkEdge_NetworkX as Edge # Edge class

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
        self.contact_network = DiGraph()
        self.name_to_num = {}       # map original node names to numbers
        self.num_to_name = []       # map numbers to original node names
        self.infected_nodes = set() # store numbers of infected nodes
        self.transmissions = []     # store u->v transmission as (u,v,time)

        # read in Contact Network as node+edge list
        for line in edge_list:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            parts = line.split('\t')

            # add node to contact network
            if parts[0] == 'NODE':
                name = parts[1]
                if name in self.name_to_num:
                    raise ValueError("Node %r already exists!" % name)
                num = len(self.num_to_name)
                self.name_to_num[name] = num
                self.num_to_name.append(name)
                self.contact_network.add_node(num)
                if parts[2] == '.':
                    self.contact_network.node[num]['attribute'] = set()
                else:
                    self.contact_network.node[num]['attribute'] = set(parts[2].split(','))
                self.contact_network.node[num]['infections'] = []
                self.contact_network.node[num]['infection_trees'] = []

            # add edge to contact network
            elif parts[0] == 'EDGE':
                uName = parts[1]
                if uName not in self.name_to_num:
                    raise ValueError("Node %r does not exist!" % uName)
                vName = parts[2]
                if vName not in self.name_to_num:
                    raise ValueError("Node %r does not exist!" % vName)
                uNum = self.name_to_num[uName]
                vNum = self.name_to_num[vName]
                self.contact_network.add_edge(uNum,vNum)
                if parts[3] == '.':
                    self.contact_network.edge[uNum][vNum]['attribute'] = set()
                else:
                    self.contact_network.edge[uNum][vNum]['attribute'] = set(parts[3].split(','))
                if parts[4] == 'u': # undirected edge, so add v to u too
                    self.contact_network.add_edge(vNum,uNum)
                    self.contact_network.edge[vNum][uNum]['attribute'] = self.contact_network.edge[uNum][vNum]['attribute']

            # invalid type
            else:
                raise ValueError("Invalid type in list: %r" % parts[0])

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
            yield Node(self.contact_network, self.num_to_name[node], node)

    def edges_iter(self):
        for edge in self.contact_network.edges():
            uNum,vNum = edge
            attr = self.contact_network.edge[uNum][vNum]['attribute']
            u = Node(self.contact_network, self.num_to_name[uNum], uNum)
            v = Node(self.contact_network, self.num_to_name[vNum], vNum)
            yield Edge(u,v,attr)

    def get_transmissions(self):
        return self.transmissions

def check():
    '''
    Check ``ContactNetwork_NetworkX`` for validity
    '''
    pass

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    check()