#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkEdge" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from ContactNetworkEdge import ContactNetworkEdge
from ContactNetworkNode import ContactNetworkNode
import FAVITES_GlobalContext as GC

class ContactNetworkEdge_PANGEA(ContactNetworkEdge):
    def init():
        pass

    def cite():
        return GC.CITATION_PANGEA

    def __init__(self, u, v, attr):
        assert isinstance(u, ContactNetworkNode), "u is not a ContactNetworkNode"
        assert isinstance(v, ContactNetworkNode), "v is not a ContactNetworkNode"
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
    pass