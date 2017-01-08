#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module, where a source node is randomly picked from the
infected nodes in the Contact Network, and one of its outgoing edges are
randomly picked for the infection.
'''
from TransmissionNodeSample import TransmissionNodeSample # abstract TransmissionNodeSample class
from ContactNetwork import ContactNetwork                 # to verify contact_network
import FAVITES_GlobalContext as GC
from random import sample                                         # to randomly sample nodes

class TransmissionNodeSample_RandomMultiInfection(TransmissionNodeSample):
    def init():
        pass
        
    def sample_nodes(time):
        source = sample(GC.contact_network.get_infected_nodes(), 1)[0]
        target = sample(GC.contact_network.get_edges_from(source), 1)[0].get_to()
        while target == source:
            target = sample(GC.contact_network.get_edges_from(source), 1)[0].get_to()
        return source,target