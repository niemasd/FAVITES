#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph is generated under the
Connected Watts-Strogatz model.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from os.path import expanduser

class ContactNetworkGenerator_WattsStrogatzConnected(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global connected_watts_strogatz_graph
            from networkx import connected_watts_strogatz_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        assert isinstance(GC.wsc_k, int), "wsc_k must be an integer"
        assert GC.wsc_k >= 2, "wsc_k must be at least 2"
        GC.wsc_prob = float(GC.wsc_prob)
        assert GC.wsc_prob >= 0 and GC.wsc_prob <= 1, "wsc_prob must be between 0 and 1"
        if GC.wsc_tries is None or GC.wsc_tries == '':
            GC.wsc_tries = 100 # this is the NetworkX default
        else:
            assert isinstance(GC.wsc_tries, int) and GC.wsc_tries > 0, "wsc_tries must be a positive integer"

    def get_edge_list():
        cn = connected_watts_strogatz_graph(GC.num_cn_nodes, GC.wsc_k, GC.wsc_prob, tries=GC.wsc_tries, seed=GC.random_number_seed)
        if GC.random_number_seed is not None:
            GC.random_number_seed += 1
        out = GC.nx2favites(cn, 'u')
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        return out