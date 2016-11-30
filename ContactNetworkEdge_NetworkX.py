#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkEdge" module, implemented with NetworkX
'''
from ContactNetworkEdge import ContactNetworkEdge # abstract ContactNetworkEdge class
from ContactNetworkNode import ContactNetworkNode # to verify nodes
import networkx as nx                             # using NetworkX to implement

class ContactNetworkEdge_NetworkX(ContactNetworkEdge):
    '''
    Implement the ``ContactNetworkEdge`` abstract class using NetworkX

    Attributes
    ----------
    u : ContactNetworkNode
        The ``ContactNetworkNode'' object from which this edge is leaving
    v : ContactNetworkNode
        The ``ContactNetworkNode'' object to which this edge is going
    attr : set of str
        The attribute(s) of this ``ContactNetworkEdge'' object

    '''

    def __init__(self, u, v, attr):
        '''
        Construct a new ``ContactNetworkEdge_NetworkX`` object

        Parameters
        ----------
        graph : Graph
            The NetworkX graph in which this node exists
        node : Node
            The NetworkX node encapsulated by this object

        '''
        assert isinstance(u, ContactNetworkNode), "u is not a ContactNetworkNode"
        assert isinstance(v, ContactNetworkNode), "v is not a ContactNetworkNode"
        assert isinstance(attr, set), "attr is not a set"
        for item in attr:
            assert isinstance(item, str), "attr contains a non-string item"
        self.u = u
        self.v = v
        self.attr = attr

    def __str__(self):
        return '%r -> %r : %s' % (str(self.u), str(self.v), str(self.attr))

    def get_attribute(self):
        return self.attr

    def get_from(self):
        return self.u

    def get_to(self):
        return self.v

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    pass