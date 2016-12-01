#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, where seed sequences are randomly generated and infect
the node at time 0
'''
import FAVITES_Global                             # for global access variables
from SeedSequence import SeedSequence             # abstract SeedSequence class
from ContactNetworkNode import ContactNetworkNode # to verify node
from random import choice                         # randomly choose nucleotides

class SeedSequence_Random(SeedSequence):
    '''
    Implement the ``SeedSequence'' module by randomly selecting seed sequences
    and infecting ``node'' at time 0
    '''

    def infect(node):
        assert isinstance(node, ContactNetworkNode), "node is not a ContactNetworkNode object"
        k = FAVITES_Global.seed_sequence_length
        assert isinstance(k, int), "Specified SeedSequenceLength is not an integer"
        sequence = ''.join([choice('ACGT') for _ in range(k)])
        node.infect(0,sequence)