#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, where seed sequences are randomly generated and infect
the node at time 0
'''
from SeedSequence import SeedSequence             # abstract SeedSequence class
from ContactNetworkNode import ContactNetworkNode # to verify node
import FAVITES_GlobalContext as GC
from random import choice                                 # randomly choose nucleotides

class SeedSequence_Random(SeedSequence):
    '''
    Implement the ``SeedSequence'' module by randomly selecting seed sequences
    and infecting ``node'' at time 0
    '''

    def init():
        pass

    def generate():
        k = GC.seed_sequence_length
        assert isinstance(k, int), "Specified SeedSequenceLength is not an integer"
        return ''.join([choice('ACGT') for _ in range(k)])