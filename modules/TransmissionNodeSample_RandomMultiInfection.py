#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module, where nodes are randomly selected with equal
probability and nodes are allowed to be infected multiple times.
'''
from TransmissionNodeSample import TransmissionNodeSample # abstract TransmissionNodeSample class
from ContactNetwork import ContactNetwork                 # to verify contact_network
import FAVITES_GlobalContext as GC
from random import sample                                         # to randomly sample nodes

class TransmissionNodeSample_RandomMultiInfection(TransmissionNodeSample):
    def sample_nodes(time):
        source = sample(GC.contact_network.get_infected_nodes(), 1)[0]
        target = sample(GC.contact_network.get_nodes(), 1)[0]
        while target == source:
            target = sample(GC.contact_network.get_nodes(), 1)[0]
        return source,target

    # THIS UNDERMINES THE CONTACT NETWORK! SHOULD INSTEAD RANDOMLY PICK EDGE
    # FROM CONTACT NETWORK