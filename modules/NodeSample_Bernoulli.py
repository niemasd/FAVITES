#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeSample" module, where transmission source node is chosen to be sampled or
not via a Bernoulli distribution with a user-specified probability of success.
If a source node is chosen, ALL transmissions from that node will be outputted,
and if not, NONE of the transmissions from that node will be outputted.
'''
from NodeSample import NodeSample # abstract NodeSample class
from random import random # for random number generator
import FAVITES_GlobalContext as GC

class NodeSample_Bernoulli(NodeSample):
    def init():
        GC.node_sample_prob = float(GC.node_sample_prob)

    def subsample_transmission_network():
        all_transmissions = GC.contact_network.get_transmissions()
        source_trans = {}
        for t in all_transmissions:
            if t[0] not in source_trans:
                source_trans[t[0]] = []
            source_trans[t[0]].append(t)
        out = []
        for source in source_trans:
            if random() < GC.node_sample_prob:
                for t in source_trans[source]:
                    out.append(t)
        return out