#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where seeds are randomly selected with equal probability
all at time t = 0
'''
import FAVITES_GlobalContext as GC                # for global access variables
from SeedSelection import SeedSelection   # abstract SeedSelection class
from ContactNetwork import ContactNetwork # to verify contact_network
from random import sample                         # to randomly sample seed nodes

class SeedSelection_Random(SeedSelection):
    '''
    Implement the ``SeedSelection'' module with uniform distribution on nodes
    all at time t = 0
    '''

    def init():
        GC.num_seeds = int(GC.num_seeds)
        if GC.num_seeds < 1:
            print("ERROR: Must have at least 1 seed node")
            exit(-1)

    def select_seeds():
        nodes = [node for node in GC.contact_network.nodes_iter()]
        seed_nodes = sample(nodes, GC.num_seeds)
        seed_times = [0.0 for node in nodes]
        return seed_nodes, seed_times