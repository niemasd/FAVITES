#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkNode" module, implemented with NetworkX
'''
import FAVITES_Global                             # for global access variables
from ContactNetworkNode import ContactNetworkNode # abstract ContactNetworkNode class
from Tree import Tree                             # to validate trees
from networkx import DiGraph                      # to validate graph

class ContactNetworkNode_NetworkX(ContactNetworkNode):
    '''
    Implement the ``ContactNetworkNode`` abstract class using NetworkX

    Attributes
    ----------
    graph : DiGraph
        The NetworkX DiGraph in which this node exists
    infected : bool
        True if this node is infected, otherwise False
    name : str
        The name of this node
    num : int
        The number of this node
    '''

    def __init__(self, graph, name, num):
        '''
        Construct a new ``ContactNetworkNode_NetworkX`` object

        Parameters
        ----------
        graph : Graph
            The NetworkX graph in which this node exists
        node : Node
            The NetworkX node encapsulated by this object
        '''
        assert isinstance(graph, DiGraph), "graph is not a NetworkX DiGraph"
        assert isinstance(name, str), "name is not a string"
        assert isinstance(num, int), "num is not an integer"
        self.graph = graph
        self.name = name
        self.num = num
        self.infected = False

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_attribute(self):
        return self.graph.node[self.num]['attribute']

    def get_infections(self):
        return self.graph.node[self.num]['infections']

    def num_infections(self):
        return len(self.get_infections())

    def infect(self, time, sequence):
        assert isinstance(time, int)
        assert isinstance(sequence, str)
        Tree = FAVITES_Global.modules['Tree']
        self.graph.node[self.num]['infections'].append((time, sequence, Tree()))
        self.infected = True

    def is_infected(self):
        return self.infected

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    pass