#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeSample" module, perfect sampling
'''
from NodeSample import NodeSample # abstract NodeSample class
import FAVITES_GlobalContext as GC

class NodeSample_Perfect(NodeSample):
    def init():
        pass

    def subsample_transmission_network():
        return GC.contact_network.get_infected_nodes()