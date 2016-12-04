#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where seeds are randomly selected with equal probability
'''
from modules import FAVITES_Global                # for global access variables
from modules.SeedSelection import SeedSelection   # abstract SeedSelection class
from modules.ContactNetwork import ContactNetwork # to verify contact_network
from random import sample                         # to randomly sample seed nodes

class SeedSelection_Random(SeedSelection):
    '''
    Implement the ``SeedSelection'' module with uniform distribution on nodes
    '''

    def select_seed_nodes():
        nodes = [node for node in FAVITES_Global.contact_network.nodes_iter()]
        return sample(nodes, FAVITES_Global.num_seeds)