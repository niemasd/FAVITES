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

class ContactNetworkGenerator_ConnectedWattsStrogatz(ContactNetworkGenerator):
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
        assert isinstance(GC.cws_k, int), "cws_k must be an integer"
        assert GC.cws_k >= 2, "cws_k must be at least 2"
        GC.cws_prob = float(GC.cws_prob)
        assert GC.cws_prob >= 0 and GC.cws_prob <= 1, "cws_prob must be between 0 and 1"
        if GC.cws_tries is None or GC.cws_tries == '':
            GC.cws_tries = 100 # this is the NetworkX default
        else:
            assert isinstance(GC.cws_tries, int) and GC.cws_tries > 0, "cws_tries must be a positive integer"

    def get_edge_list():
        cn = connected_watts_strogatz_graph(GC.num_cn_nodes, GC.cws_k, GC.cws_prob, tries=GC.cws_tries, seed=GC.random_number_seed)
        if GC.random_number_seed is not None:
            GC.random_number_seed += 1
        out = GC.nx2favites(cn, 'u')
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        return out