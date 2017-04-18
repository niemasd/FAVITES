#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where seeds are randomly selected with equal probability
'''
from SeedSelection import SeedSelection
import FAVITES_GlobalContext as GC
from random import sample

class SeedSelection_Random(SeedSelection):
    '''
    Implement the ``SeedSelection'' module with uniform distribution on nodes
    '''

    def init():
        GC.num_seeds = int(GC.num_seeds)
        assert GC.num_seeds >= 1, "Must have at least 1 seed node"

    def select_seeds():
        nodes = [node for node in GC.contact_network.nodes_iter()]
        seed_nodes = sample(nodes, GC.num_seeds)
        return seed_nodes