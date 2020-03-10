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

    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.num_seeds = int(GC.num_seeds)
        assert GC.num_seeds >= 1, "Must have at least 1 seed node"
        assert isinstance(GC.seed_seqs, list), "seed_seqs must be a list of strings"
        assert len(GC.seed_seqs) == GC.num_seeds, "seed_seqs must have exactly num_seeds sequences!"
        for s in GC.seed_seqs:
            assert '-' not in s, "Seed sequences cannot have gaps"
        GC.seed_seqs_num = 0

    def generate():
        seq = GC.seed_seqs[GC.seed_seqs_num]
        GC.seed_seqs_num += 1
        return seq

    def merge_trees():
        return [],[]
