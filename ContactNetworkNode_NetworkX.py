#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkNode" module, implemented with NetworkX
'''
from ContactNetworkNode import ContactNetworkNode # abstract ContactNetworkNode class
import networkx as nx                             # using NetworkX to implement

class ContactNetworkNode_NetworkX(ContactNetworkNode):
    '''
    Implement the ``ContactNetworkNode`` abstract class using NetworkX

    Attributes
    ----------
    node : node
        The NetworkX node encapsulated by this object

    '''

    def __init__(self, graph, node):
        '''
        Construct a new ``ContactNetworkNode_NetworkX`` object

        Parameters
        ----------
        graph : Graph
            The NetworkX graph in which this node exists
        node : Node
            The NetworkX node encapsulated by this object

        '''
        self.graph = graph
        self.node = node

    def get_name(self):
        return self.node

    def get_attribute(self):
        return self.graph.node[self.node]['attribute']

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    pass