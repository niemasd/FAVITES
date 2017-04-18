#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, where seed sequences are randomly generated and infect
the node at time 0
'''
from SeedSequence import SeedSequence
import FAVITES_GlobalContext as GC
from random import choice

class SeedSequence_Random(SeedSequence):
    '''
    Implement the ``SeedSequence'' module by randomly selecting seed sequences
    and infecting ``node'' at time 0
    '''

    def init():
        assert isinstance(GC.seed_sequence_length, int), "Specified SeedSequenceLength is not an integer"

    def generate():
        return ''.join([choice('ACGT') for _ in range(GC.seed_sequence_length)])