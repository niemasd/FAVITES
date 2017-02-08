#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, where the user specifies the seed sequences
'''
from SeedSequence import SeedSequence
import FAVITES_GlobalContext as GC

class SeedSequence_User(SeedSequence):
    '''
    Implement the ``SeedSequence'' module, where the user specifies the seed
    sequences
    '''

    def init():
        GC.num_seeds = int(GC.num_seeds)
        assert GC.num_seeds >= 1, "Must have at least 1 seed node"
        assert len(GC.seed_seqs) == GC.num_seeds, "seed_seqs must have exactly num_seeds sequences!"
        GC.seed_seqs_num = 0

    def generate():
        seq = GC.seed_seqs[num]
        GC.seed_seqs_num += 1
        return seq