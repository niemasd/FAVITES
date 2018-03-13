#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph is generated under the
Erdos-Renyi model.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from os.path import expanduser

class ContactNetworkGenerator_ErdosRenyi(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global fast_gnp_random_graph
            from networkx import fast_gnp_random_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        GC.er_prob = float(GC.er_prob)
        assert GC.er_prob >= 0 and GC.er_prob <= 1, "er_prob must be between 0 and 1"
        GC.d_or_u = GC.d_or_u.strip()
        assert GC.d_or_u == 'd' or GC.d_or_u == 'u', '"d_or_u" must be either "d" or "u"'

    def get_edge_list():
        du = GC.d_or_u == 'd'
        cn = fast_gnp_random_graph(GC.num_cn_nodes, GC.er_prob, directed=du, seed=GC.random_number_seed)
        if GC.random_number_seed is not None:
            GC.random_number_seed += 1
        out = GC.nx2favites(cn, GC.d_or_u)
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        return out