#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph is generated under the
Barabasi-Albert model.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from os.path import expanduser

class ContactNetworkGenerator_PowerlawClusterGraph(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global powerlaw_cluster_graph
            from networkx import powerlaw_cluster_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        assert isinstance(GC.pcg_m, int), "pcg_m must be an integer"
        assert 1 <= GC.pcg_m <= GC.num_cn_nodes, "pcg_m must be in the range [1,num_cn_nodes]"
        GC.pcg_p = float(GC.pcg_p)
        assert 0 <= GC.pcg_p <= 1, "pcg_p must be between 0 and 1"

    def get_edge_list():
        cn = powerlaw_cluster_graph(GC.num_cn_nodes, GC.pcg_m, GC.pcg_p, seed=GC.random_number_seed)
        if GC.random_number_seed is not None:
            GC.random_number_seed += 1
        out = GC.nx2favites(cn, 'u')
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        return out