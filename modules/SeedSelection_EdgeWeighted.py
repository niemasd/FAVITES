#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where the probability at which a node is chosen is
weighted by its degree
'''
from SeedSelection import SeedSelection
import FAVITES_GlobalContext as GC
from random import choice

class SeedSelection_EdgeWeighted(SeedSelection):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.num_seeds = int(GC.num_seeds)
        assert GC.num_seeds >= 1, "Must have at least 1 seed node"

    def select_seeds():
        edges = [edge for edge in GC.contact_network.edges_iter()]
        seed_nodes = set()
        while len(seed_nodes) < GC.num_seeds:
            edge = choice(edges)
            seed_nodes.add(choice((edge.get_from(), edge.get_to())))
        return list(seed_nodes)
