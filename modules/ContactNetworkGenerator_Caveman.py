#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, creating a Caveman graph
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser

class ContactNetworkGenerator_Caveman(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global caveman_graph
            from networkx import caveman_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.cave_num_cliques, int), "cave_num_cliques must be an integer"
        assert GC.cave_num_cliques > 0, "Must have at least 1 clique"
        assert isinstance(GC.cave_clique_size, int), "cave_clique_size must be an integer"
        assert GC.cave_clique_size > 0, "Cliques must contain at least 1 node"

    def get_edge_list():
        cn = caveman_graph(GC.cave_num_cliques, GC.cave_clique_size)
        out = GC.nx2favites(cn, 'u')
        f = open(expanduser("%s/contact_network.txt" % GC.out_dir),'w')
        f.write('\n'.join(out))
        f.close()
        return out