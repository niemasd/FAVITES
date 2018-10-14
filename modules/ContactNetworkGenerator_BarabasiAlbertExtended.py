#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph is generated under the
Extended Barabasi-Albert model.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from os.path import expanduser

class ContactNetworkGenerator_BarabasiAlbertExtended(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global extended_barabasi_albert_graph
            from networkx import extended_barabasi_albert_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        assert isinstance(GC.num_edges_from_new, int), "num_edges_from_new must be an integer"
        assert 1 <= GC.num_edges_from_new < GC.num_cn_nodes, "num_edges_from_new must be in the range [1,num_cn_nodes)"
        GC.bae_p = float(GC.bae_p)
        assert 0 <= GC.bae_p <= 1, "bae_p must be between 0 and 1"
        GC.bae_q = float(GC.bae_q)
        assert 0 <= GC.bae_q <= 1, "bae_q must be between 0 and 1"
        assert GC.bae_p + GC.bae_q < 1, "bae_p + bae_q must be less than 1"

    def get_edge_list():
        cn = extended_barabasi_albert_graph(GC.num_cn_nodes, GC.num_edges_from_new, GC.bae_p, GC.bae_q, seed=GC.random_number_seed)
        if GC.random_number_seed is not None:
            GC.random_number_seed += 1
        out = GC.nx2favites(cn, 'u')
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        return out