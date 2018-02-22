#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph that is generated is the
Barbell Graph.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser

class ContactNetworkGenerator_Barbell(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global barbell_graph
            from networkx import barbell_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.barbell_m1, int), "barbell_m1 must be an integer"
        assert GC.barbell_m1 > 1, "barbell_m1 must be greater than 1"
        assert isinstance(GC.barbell_m2, int), "barbell_m2 must be an integer"
        assert GC.barbell_m2 >= 0, "barbell_m2 must be at least 0"

    def get_edge_list():
        cn = barbell_graph(GC.barbell_m1, GC.barbell_m2)
        out = GC.nx2favites(cn, 'u')
        f = open(expanduser("%s/contact_network.txt" % GC.out_dir),'w')
        f.write('\n'.join(out))
        f.close()
        GC.cn_communities = [{i for i in range(GC.barbell_m1)}, {i for i in range(GC.barbell_m1+GC.barbell_m2, 2*GC.barbell_m1+GC.barbell_m2)}] # only left and right communities, not the path
        f = open(expanduser("%s/contact_network_partitions.txt" % GC.out_dir),'w')
        f.write(str(GC.cn_communities))
        f.close()
        GC.cn_communities = [{str(i) for i in c} for c in GC.cn_communities]
        return out