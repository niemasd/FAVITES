#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, creating a Relaxed Caveman graph
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser

class ContactNetworkGenerator_CavemanRelaxed(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global relaxed_caveman_graph
            from networkx import relaxed_caveman_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.cave_num_cliques, int), "cave_num_cliques must be an integer"
        assert GC.cave_num_cliques > 0, "Must have at least 1 clique"
        assert isinstance(GC.cave_clique_size, int), "cave_clique_size must be an integer"
        assert GC.cave_clique_size > 0, "Cliques must contain at least 1 node"
        GC.cave_prob = float(GC.cave_prob)
        assert GC.cave_prob >= 0 and GC.cave_prob <= 1, "cave_prob must be between 0 and 1"

    def get_edge_list():
        cn = relaxed_caveman_graph(GC.cave_num_cliques, GC.cave_clique_size, GC.cave_prob, seed=GC.random_number_seed)
        if GC.random_number_seed is not None:
            GC.random_number_seed += 1
        out = GC.nx2favites(cn, 'u')
        f = open(expanduser("%s/contact_network.txt" % GC.out_dir),'w')
        f.write('\n'.join(out))
        f.close()
        GC.cn_communities = [{c*GC.cave_clique_size+i for i in range(GC.cave_clique_size)} for c in range(GC.cave_num_cliques)]
        f = open(expanduser("%s/contact_network_partitions.txt" % GC.out_dir),'w')
        f.write(str(GC.cn_communities))
        f.close()
        GC.cn_communities = [{str(i) for i in c} for c in GC.cn_communities]
        return out