#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module, where a source node is randomly picked from the
infected nodes in the Contact Network, and one of its outgoing edges are
randomly picked for the infection. A node can only be infected once.
'''
from TransmissionNodeSample import TransmissionNodeSample
import FAVITES_GlobalContext as GC
from random import sample

class TransmissionNodeSample_RandomSingleInfection(TransmissionNodeSample):
    def init():
        pass

    def sample_nodes(time):
        infected = GC.contact_network.get_infected_nodes()
        source = sample(infected,1)[0]
        neighbors = {source:{edge.get_to() for edge in GC.contact_network.get_edges_from(source) if not edge.get_to().is_infected()}}
        while len(neighbors[source]) == 0:
            infected.remove(source)
            if len(infected) == 0:
                return None,None
            source = sample(infected,1)[0]
            neighbors[source] = {edge.get_to() for edge in GC.contact_network.get_edges_from(source) if not edge.get_to().is_infected()}
        target = sample(neighbors[source],1)[0]
        return source,target