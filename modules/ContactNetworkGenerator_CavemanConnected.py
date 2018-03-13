#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, creating a Connected Caveman graph
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from os.path import expanduser

class ContactNetworkGenerator_CavemanConnected(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global connected_caveman_graph
            from networkx import connected_caveman_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.cave_num_cliques, int), "cave_num_cliques must be an integer"
        assert GC.cave_num_cliques > 0, "Must have at least 1 clique"
        assert isinstance(GC.cave_clique_size, int), "cave_clique_size must be an integer"
        assert GC.cave_clique_size > 0, "Cliques must contain at least 1 node"

    def get_edge_list():
        cn = connected_caveman_graph(GC.cave_num_cliques, GC.cave_clique_size)
        out = GC.nx2favites(cn, 'u')
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        GC.cn_communities = [{c*GC.cave_clique_size+i for i in range(GC.cave_clique_size)} for c in range(GC.cave_num_cliques)]
        f = gopen(expanduser("%s/contact_network_partitions.txt.gz" % GC.out_dir),'wb',9)
        f.write(str(GC.cn_communities).encode()); f.write(b'\n')
        f.close()
        GC.cn_communities = [{str(i) for i in c} for c in GC.cn_communities]
        return out