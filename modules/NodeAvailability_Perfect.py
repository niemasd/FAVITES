#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeAvailability" module, perfect sampling
'''
from NodeAvailability import NodeAvailability
import FAVITES_GlobalContext as GC

class NodeAvailability_Perfect(NodeAvailability):
    def init():
        pass

    def subsample_transmission_network():
        return GC.contact_network.get_infected_nodes()