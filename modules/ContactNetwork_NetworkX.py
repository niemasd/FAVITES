#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetwork" module, implemented with NetworkX
'''
from ContactNetwork import ContactNetwork
from ContactNetworkNode_NetworkX import ContactNetworkNode_NetworkX as Node
from ContactNetworkEdge_NetworkX import ContactNetworkEdge_NetworkX as Edge
import FAVITES_GlobalContext as GC
from copy import copy

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
    nodes : set of ContactNetworkNodes
        Set containing all of the nodes in this ``ContactNetwork''
    num_to_name : dict
        Dictionary mapping numbers to original node names
    transmissions : list
        List of transmission events as (u,v,time) tuples
    uninfected_nodes : set of ContactNetworkNodes
        Set contianing the nodes that have not yet been infected
    '''

    def init():
        try:
            global DiGraph
            from networkx import DiGraph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"

    def __init__(self, edge_list=None):
        # if ModuleFactory is just testing, do nothing
        if edge_list is None:
            return

        # set up NetworkX and graph
        self.contact_network = DiGraph()
        self.name_to_num = {}         # map original node names to numbers
        self.num_to_name = []         # map numbers to original node names
        self.nodes = set()            # store all nodes
        self.uninfected_nodes = set() # store uninfected nodes
        self.infected_nodes = set()   # store infected nodes
        self.transmissions = []       # store u->v transmission as (u,v,time)

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
                    self.contact_network.node[num]['attribute'] = set([e.strip().upper() for e in parts[2].split(',')])
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

        # create sets of nodes
        for node in self.contact_network.nodes():
            self.nodes.add(Node(self, self.num_to_name[node], node))
        for node in self.nodes:
            self.uninfected_nodes.add(node)

    def num_transmissions(self):
        return len(self.transmissions)

    def num_nodes(self):
        return len(self.nodes)

    def get_nodes(self):
        return copy(self.nodes)

    def get_node(self, name):
        return Node(self, name, self.name_to_num[name])

    def num_infected_nodes(self):
        return len(self.infected_nodes)

    def get_infected_nodes(self):
        return copy(self.infected_nodes)

    def num_uninfected_nodes(self):
        return len(self.uninfected_nodes)

    def get_uninfected_nodes(self):
        return copy(self.uninfected_nodes)

    def num_edges(self):
        return self.contact_network.number_of_edges()

    def nodes_iter(self):
        for node in self.nodes:
            yield node

    def edges_iter(self):
        for edge in self.contact_network.edges():
            uNum,vNum = edge
            attr = self.contact_network.edge[uNum][vNum]['attribute']
            u = Node(self, self.num_to_name[uNum], uNum)
            v = Node(self, self.num_to_name[vNum], vNum)
            yield Edge(u,v,attr)

    def get_edges_from(self, node):
        nx_edges = self.contact_network.out_edges(self.name_to_num[node.get_name()])
        return [Edge(node, Node(self, self.num_to_name[vNum], vNum), self.contact_network.edge[uNum][vNum]['attribute']) for uNum,vNum in nx_edges]

    def get_edges_to(self,node):
        nx_edges = self.contact_network.in_edges(self.name_to_num[node.get_name()])
        return [Edge(Node(self, self.num_to_name[uNum], uNum), node, self.contact_network.edge[uNum][vNum]['attribute']) for uNum,vNum in nx_edges]

    def get_transmissions(self):
        return copy(self.transmissions)

    def add_transmission(self,u,v,time):
        assert isinstance(u, Node), "u is not a ContactNetworNode_NetworkX"
        assert isinstance(v, Node), "v is not a ContactNetworNode_NetworkX"
        self.transmissions.append((u,v,time))
        if u != v:
            self.add_to_infected(v)

    def add_to_infected(self,node):
        assert isinstance(node, Node), "node is not a ContactNetworNode_NetworkX"
        assert node.is_infected(), "node is not infected! Infect before moving"
        if node in self.uninfected_nodes:
            self.uninfected_nodes.remove(node)
        self.infected_nodes.add(node)

    def remove_from_infected(self,node):
        assert isinstance(node, Node), "node is not a ContactNetworNode_NetworkX"
        assert not node.is_infected(), "node is infected! Uninfect before moving"
        self.infected_nodes.discard(node)
        self.uninfected_nodes.add(node)

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