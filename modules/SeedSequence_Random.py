#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, where seed sequences are randomly generated and infect
the node at time 0
'''
from modules import FAVITES_Global                        # for global access variables
from modules.SeedSequence import SeedSequence             # abstract SeedSequence class
from modules.ContactNetworkNode import ContactNetworkNode # to verify node
from random import choice                                 # randomly choose nucleotides

class SeedSequence_Random(SeedSequence):
    '''
    Implement the ``SeedSequence'' module by randomly selecting seed sequences
    and infecting ``node'' at time 0
    '''

    def generate():
        k = FAVITES_Global.seed_sequence_length
        assert isinstance(k, int), "Specified SeedSequenceLength is not an integer"
        return ''.join([choice('ACGT') for _ in range(k)])