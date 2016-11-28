#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module
'''
from SeedSequence import SeedSequence

class SeedSequence_DUMMY(SeedSequence):
    '''
    Dummy class implementing the ``SeedSequence`` module

    Methods
    -------
    evolve(node)
        Evolve a phylogeny and sequences on ``node''
    '''

    def evolve(node):
        print()
        print("Using SeedSequence_DUMMY, so nothing is done.")
        print("Implement a real SeedSequence module before release!!!")