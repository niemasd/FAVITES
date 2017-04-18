#! /usr/bin/env python3
'''
Niema Moshiri 2016

"PostValidation" module, dummy implementation
'''
from PostValidation import PostValidation

class PostValidation_Dummy(PostValidation):
    def init():
        pass

    def score_transmission_network():
        return "DUMMY"

    def score_phylogenetic_tree(tree):
        return "DUMMY"

    def score_sequences(seqs):
        return "DUMMY"