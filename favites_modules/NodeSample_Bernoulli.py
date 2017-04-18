#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeSample" module, where transmission source node is chosen to be sampled or
not via a Bernoulli distribution with a user-specified probability of success.
If a source node is chosen, ALL transmissions from that node will be outputted,
and if not, NONE of the transmissions from that node will be outputted.
'''
from NodeSample import NodeSample
import FAVITES_GlobalContext as GC
from random import random

class NodeSample_Bernoulli(NodeSample):
    def init():
        GC.node_sample_prob = float(GC.node_sample_prob)

    def subsample_transmission_network():
        nodes = GC.contact_network.get_infected_nodes()
        return [n for n in nodes if random() < GC.node_sample_prob]