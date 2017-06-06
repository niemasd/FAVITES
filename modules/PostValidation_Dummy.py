#! /usr/bin/env python3
'''
Niema Moshiri 2016

"PostValidation" module, dummy implementation
'''
from PostValidation import PostValidation
import FAVITES_GlobalContext as GC

class PostValidation_Dummy(PostValidation):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def score_transmission_network():
        return "DUMMY"

    def score_phylogenetic_tree(tree):
        return "DUMMY"

    def score_sequences(seqs):
        return "DUMMY"