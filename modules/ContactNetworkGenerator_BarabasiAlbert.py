#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph is generated under the
Barabasi-Albert model.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser

class ContactNetworkGenerator_BarabasiAlbert(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global barabasi_albert_graph
            from networkx import barabasi_albert_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        assert isinstance(GC.num_edges_from_new, int), "num_edges_from_new must be an integer"
        assert GC.num_edges_from_new > 0, "Must have at least 1 edge to attach from a new node to existing nodes"

    def get_edge_list():
        cn = barabasi_albert_graph(GC.num_cn_nodes, GC.num_edges_from_new)
        out = GC.nx2favites(cn, 'u')
        f = open(expanduser("%s/contact_network.txt" % GC.out_dir),'w')
        f.write('\n'.join(out))
        f.close()
        return out