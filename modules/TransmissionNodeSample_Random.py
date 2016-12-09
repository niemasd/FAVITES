#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module, where nodes are randomly selected with equal
probability
'''
from TransmissionNodeSample import TransmissionNodeSample # abstract TransmissionNodeSample class
from ContactNetwork import ContactNetwork                 # to verify contact_network
import FAVITES_GlobalContext as GC
from random import sample                                         # to randomly sample nodes

class TransmissionNodeSample_Random(TransmissionNodeSample):
    '''
    Implement the ``TransmissionNodeSample'' module with uniform distribution on nodes
    '''

    def sample_nodes():
        source = sample(GC.contact_network.get_infected_nodes(), 1)[0]
        target = sample(GC.contact_network.get_uninfected_nodes(), 1)[0]
        return source,target