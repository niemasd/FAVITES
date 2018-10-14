#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph is generated under the
d-Regular Graph model.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from os.path import expanduser

class ContactNetworkGenerator_RegularGraph(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global random_regular_graph
            from networkx import random_regular_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        assert isinstance(GC.cn_degree, int), "cn_degree must be an integer"
        assert GC.cn_degree > 0, "cn_degree must be positive"
        assert GC.num_cn_nodes*GC.cn_degree % 2 == 0, "num_cn_nodes*cn_degree must be even"
        assert GC.cn_degree < GC.num_cn_nodes, "cn_degree must be less than num_cn_nodes"

    def get_edge_list():
        cn = random_regular_graph(GC.cn_degree, GC.num_cn_nodes, seed=GC.random_number_seed)
        if GC.random_number_seed is not None:
            GC.random_number_seed += 1
        out = GC.nx2favites(cn, 'u')
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        return out