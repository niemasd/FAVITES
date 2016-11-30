#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where seeds are randomly selected with equal probability
'''
from SeedSelection import SeedSelection   # abstract SeedSelection class
from ContactNetwork import ContactNetwork # to verify contact_network
from random import sample                 # to randomly sample seed nodes

class SeedSelection_Random(SeedSelection):
    '''
    Implement the ``SeedSelection'' module with uniform distribution on nodes
    '''

    def select_seed_nodes(user_input, contact_network):
        assert isinstance(user_input, dict), "user_input is not a dictionary"
        assert isinstance(contact_network, ContactNetwork), "contact_network is not a ContactNetwork object"
        n = user_input['num_seeds']
        nodes = [node for node in contact_network.nodes_iter()]
        return sample(nodes, n)