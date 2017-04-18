#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph is generated under the
Watts-Strogatz model.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser

class ContactNetworkGenerator_WattsStrogatz(ContactNetworkGenerator):
    def init():
        try:
            global watts_strogatz_graph
            from networkx import watts_strogatz_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        assert isinstance(GC.ws_k, int), "ws_k must be an integer"
        assert GC.ws_k >= 2, "ws_k must be at least 2"
        GC.ws_prob = float(GC.ws_prob)
        assert GC.ws_prob >= 0 and GC.ws_prob <= 1, "ws_prob must be between 0 and 1"

    def get_edge_list():
        cn = watts_strogatz_graph(GC.num_cn_nodes, GC.ws_k, GC.ws_prob)
        out = GC.nx2favites(cn, 'u')
        f = open(expanduser(GC.out_dir + "/contact_network.txt"),'w')
        f.write('\n'.join(out))
        f.close()
        return out