#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, where seed sequences are randomly generated specified
nucleotide frequencies and infect the node at time 0
'''
from SeedSequence import SeedSequence
import FAVITES_GlobalContext as GC

# generate a random string of length k given stationary probabilities pi
def genString(k, pi):
    return ''.join([GC.roll(pi) for _ in range(k)])

class SeedSequence_RandomWeighted(SeedSequence):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert isinstance(GC.seed_sequence_length, int), "Specified SeedSequenceLength is not an integer"
        A = float(GC.seed_prob_A)
        C = float(GC.seed_prob_C)
        G = float(GC.seed_prob_G)
        assert A >= 0 and A <= 1, "Seed sequence probability A must be between 0 and 1"
        assert C >= 0 and C <= 1, "Seed sequence probability C must be between 0 and 1"
        assert G >= 0 and G <= 1, "Seed sequence probability G must be between 0 and 1"
        assert A+C+G <= 1, "Seed probabilities A+C+G cannot be greater than 1"
        T = 1-A-C-G
        GC.seed_nuc_probs = {'A':A, 'C':C, 'G':G, 'T':T}

    def generate():
        return genString(GC.seed_sequence_length, GC.seed_nuc_probs)

    def merge_trees():
        return [],[]