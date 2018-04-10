#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeAvailability" module, where the probability that a given ContactNetwork node is
sampled is weighted by the number of transmission events in which the node was
involved (either as the infector or the infectee).
'''
from NodeAvailability import NodeAvailability
import FAVITES_GlobalContext as GC

class NodeAvailability_TransmissionWeighted(NodeAvailability):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.node_sample_fraction = float(GC.node_sample_fraction)
        assert GC.node_sample_fraction >= 0 and GC.node_sample_fraction <= 1, "node_sample_fraction must be between 0 and 1"

    def subsample_transmission_network():
        nodes = {GC.contact_network.get_node(n) for n in GC.final_sequences}
        die = {}
        for u,v,t in GC.contact_network.get_transmissions():
            if u not in die:
                die[u] = 1
            else:
                die[u] += 1
            if v not in die:
                die[v] = 1
            else:
                die[v] += 1
        die = {n:die[n] for n in nodes if n in die}
        num_sample = GC.node_sample_fraction * len(die.keys())
        out = []
        while len(die) != 0 and len(out) < num_sample:
            n = GC.roll(die)
            out.append(n)
            die.pop(n)
        return out