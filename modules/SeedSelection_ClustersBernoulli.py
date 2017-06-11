#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where m seed individuals are chosen as follows:
- k initial seeds are chosen in an edge-weighted manner
- For each of the k initial seeds, a random walk is performed starting at the
  initial seed
  - At each non-seed node in the walk, the node is chosen as a seed with
    probability p
  - The random walk ends when m/k nodes are chosen to be seeds
'''
from SeedSelection import SeedSelection
import FAVITES_GlobalContext as GC
from random import choice,random

class SeedSelection_ClustersBernoulli(SeedSelection):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.seed_k = int(GC.seed_k)
        assert GC.seed_k >= 1, "Must have at least 1 cluster"
        GC.seed_m = int(GC.seed_m)
        assert GC.seed_m >= GC.seed_k, "The number of seeds must be at least the number of clusters"
        GC.seed_p = float(GC.seed_p)
        assert GC.seed_p > 0 and GC.seed_p <= 1, "The seed probability of success must be in the range 0 < p <= 1"

    def select_seeds():
        edges = [edge for edge in GC.contact_network.edges_iter()]
        initial_seeds = set()
        while len(initial_seeds) < GC.seed_k:
            edge = choice(edges)
            initial_seeds.add(choice((edge.get_from(), edge.get_to())))
        seed_nodes = {seed for seed in initial_seeds}
        extras = m%k
        for seed in initial_seeds:
            new_seeds = {seed}
            cap = int(GC.seed_m/GC.seed_k)
            if extras != 0:
                cap += 1
                extras -= 1
            curr = seed
            while len(new_seeds) < cap:
                curr = choice([e for e in GC.contact_network.get_edges_from(curr)]).get_to()
                if curr not in new_seeds and random() < GC.seed_p:
                    new_seeds.add(curr)
            seed_nodes.update(new_seeds)
        assert len(seed_nodes) == GC.seed_m, "ERROR: Number of seed nodes didn't equal seed_m!"
        return seed_nodes