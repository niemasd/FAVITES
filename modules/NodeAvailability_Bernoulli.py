#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeAvailability" module, where transmission source node is chosen to be sampled or
not via a Bernoulli distribution with a user-specified probability of success.
If a source node is chosen, ALL transmissions from that node will be outputted,
and if not, NONE of the transmissions from that node will be outputted.
'''
from NodeAvailability import NodeAvailability
import FAVITES_GlobalContext as GC
from random import random

class NodeAvailability_Bernoulli(NodeAvailability):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.node_sample_prob = float(GC.node_sample_prob)
        assert GC.node_sample_prob >= 0 and GC.node_sample_prob <= 1, "node_sample_prob must be between 0 and 1"

    def subsample_transmission_network():
        nodes = {GC.contact_network.get_node(n) for n in GC.final_sequences}
        return [n for n in nodes if random() < GC.node_sample_prob]