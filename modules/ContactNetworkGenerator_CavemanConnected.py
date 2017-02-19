#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, creating a Connected Caveman graph
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser
from networkx import connected_caveman_graph

class ContactNetworkGenerator_CavemanConnected(ContactNetworkGenerator):
    def init():
        assert isinstance(GC.cave_num_cliques, int), "cave_num_cliques must be an integer"
        assert GC.cave_num_cliques > 0, "Must have at least 1 clique"
        assert isinstance(GC.cave_clique_size, int), "cave_clique_size must be an integer"
        assert GC.cave_clique_size > 0, "Cliques must contain at least 1 node"

    def get_edge_list():
        cn = connected_caveman_graph(GC.cave_num_cliques, GC.cave_clique_size)
        out = GC.nx2favites(cn, 'u')
        f = open(expanduser(GC.out_dir + "/contact_network.txt"),'w')
        f.write('\n'.join(out))
        f.close()
        return out