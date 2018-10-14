#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph is generated under the
Newman-Watts-Strogatz model.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from os.path import expanduser

class ContactNetworkGenerator_NewmanWattsStrogatz(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global newman_watts_strogatz_graph
            from networkx import newman_watts_strogatz_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        assert isinstance(GC.nws_k, int), "nws_k must be an integer"
        assert GC.nws_k >= 2, "nws_k must be at least 2"
        GC.nws_prob = float(GC.nws_prob)
        assert GC.nws_prob >= 0 and GC.nws_prob <= 1, "nws_prob must be between 0 and 1"

    def get_edge_list():
        cn = newman_watts_strogatz_graph(GC.num_cn_nodes, GC.nws_k, GC.nws_prob, seed=GC.random_number_seed)
        if GC.random_number_seed is not None:
            GC.random_number_seed += 1
        out = GC.nx2favites(cn, 'u')
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        return out