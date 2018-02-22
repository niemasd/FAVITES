#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where the same number of seed individuals are randomly
chosen from each community
'''
from SeedSelection import SeedSelection
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from random import sample

class SeedSelection_CommunityRandomConstant(SeedSelection):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert MF.modules['ContactNetworkGenerator'].__name__ in GC.COMMUNITY_GENERATORS, "Must use a ContactNetworkGenerator that creates communities (%s)" % ', '.join(sorted(GC.COMMUNITY_GENERATORS))
        GC.num_seeds_per_community = int(GC.num_seeds_per_community)
        assert GC.num_seeds_per_community >= 1, "Number of per-community seeds must be a positive integer"

    def select_seeds():
        seed_nodes = [i for c in GC.cn_communities for i in sample(c,GC.num_seeds_per_community)]
        if isinstance(seed_nodes[0],str):
            seed_nodes = [GC.contact_network.get_node(i) for i in seed_nodes]
        return seed_nodes