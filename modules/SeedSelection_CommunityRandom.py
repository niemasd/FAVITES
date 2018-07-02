#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where a user-specified number of seeds is randomly
chosen from each community
'''
from SeedSelection import SeedSelection
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from random import sample

class SeedSelection_CommunityRandom(SeedSelection):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert MF.modules['ContactNetworkGenerator'].__name__ in GC.COMMUNITY_GENERATORS, "Must use a ContactNetworkGenerator that creates communities (%s)" % ', '.join(sorted(GC.COMMUNITY_GENERATORS))
        assert isinstance(GC.num_seeds_each_community, list), "num_seeds_each_community must be a list of positive integers"
        for e in GC.num_seeds_each_community:
            assert isinstance(e, int) and e >= 0, "num_seeds_each_community must be a list of non-negative integers"
        assert sum(GC.num_seeds_each_community) > 0, "Must have at least 1 seed"

    def select_seeds():
        assert len(GC.num_seeds_each_community) == len(GC.cn_communities), "The length of num_seeds_each_community does not match the number of communities"
        for i in range(len(GC.cn_communities)):
            assert GC.num_seeds_each_community[i] <= len(GC.cn_communities[i]), "The number of seeds specified for community %d (0-based indexing) is larger than the number of individuals in the community"%i
        seed_nodes = [n for i in range(len(GC.cn_communities)) for n in sample(GC.cn_communities[i],GC.num_seeds_each_community[i])]
        if isinstance(seed_nodes[0],str):
            seed_nodes = [GC.contact_network.get_node(i) for i in seed_nodes]
        return seed_nodes