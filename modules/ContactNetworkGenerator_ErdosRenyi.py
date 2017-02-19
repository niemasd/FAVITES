#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where a user-specified number of nodes are
created, and a user-specified number of edges are randomly placed on the graph
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser
from networkx import fast_gnp_random_graph

class ContactNetworkGenerator_ErdosRenyi(ContactNetworkGenerator):
    '''
    Implement the ``ContactNetworkGenerator'', loading the edge list from file
    '''

    def init():
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        GC.er_prob = float(GC.er_prob)
        assert GC.er_prob >= 0 and GC.er_prob <= 1, "er_prob must be between 0 and 1"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        GC.d_or_u = GC.d_or_u.strip()
        assert GC.d_or_u == 'd' or GC.d_or_u == 'u', '"d_or_u" must be either "d" or "u"'

    def get_edge_list():
        du = GC.d_or_u == 'd'
        cn = fast_gnp_random_graph(GC.num_cn_nodes, GC.er_prob, directed=du)
        out = GC.nx2favites(cn, GC.d_or_u)
        f = open(expanduser(GC.out_dir + "/contact_network.txt"),'w')
        f.write('\n'.join(out))
        f.close()
        return out