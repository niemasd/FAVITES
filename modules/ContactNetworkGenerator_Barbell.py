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
    def init():
        global barbell_graph
        from networkx import barbell_graph
        assert isinstance(GC.barbell_m1, int), "barbell_m1 must be an integer"
        assert GC.barbell_m1 > 1, "barbell_m1 must be greater than 1"
        assert isinstance(GC.barbell_m2, int), "barbell_m2 must be an integer"
        assert GC.barbell_m2 >= 0, "barbell_m2 must be at least 0"

    def get_edge_list():
        cn = barbell_graph(GC.barbell_m1, GC.barbell_m2)
        out = GC.nx2favites(cn, 'u')
        f = open(expanduser(GC.out_dir + "/contact_network.txt"),'w')
        f.write('\n'.join(out))
        f.close()
        return out