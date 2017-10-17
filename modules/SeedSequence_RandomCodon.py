#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, where seed sequences are randomly generated from codons
(excluding STOP) and infect the node at time 0
'''
from SeedSequence import SeedSequence
import FAVITES_GlobalContext as GC
from random import choice

class SeedSequence_RandomCodon(SeedSequence):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert isinstance(GC.seed_sequence_codon_length, int), "Specified seed_sequence_codon_length is not an integer"

    def generate():
        codons = set(GC.generate_all_kmers(3,'ACGT'))
        codons.difference_update({'TGA','TAA','TAG'}) # remove STOP codons
        codons = list(codons)
        return ''.join([choice(codons) for _ in range(GC.seed_sequence_codon_length)])

    def merge_trees():
        return []