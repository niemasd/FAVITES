#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where a user-specified number of nodes are
created, and a user-specified number of edges are randomly placed on the graph
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser
from random import sample

class ContactNetworkGenerator_RandomNumsNodeEdge(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert isinstance(GC.num_cn_nodes, int), "num_cn_nodes must be an integer"
        assert isinstance(GC.num_cn_edges, int), "num_cn_edges must be an integer"
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        assert GC.num_cn_edges > 0, "Contact network must have at least 1 edge"
        assert GC.num_cn_edges <= GC.num_cn_nodes * (GC.num_cn_nodes - 1), "If there are n contact network nodes, there cannot be more than n*(n-1) edges"
        GC.d_or_u = GC.d_or_u.strip()
        assert GC.d_or_u == 'd' or GC.d_or_u == 'u', '"d_or_u" must be either "d" or "u"'

    def get_edge_list():
        nodes = [str(i) for i in range(GC.num_cn_nodes)]
        out = ["NODE\t%s\t." % node for node in nodes]
        poss_edges = set([(u,v) for u in nodes for v in nodes if u != v])
        for _ in range(GC.num_cn_edges):
            edge = sample(poss_edges,1)[0]
            poss_edges.remove(edge)
            out.append("EDGE\t%s\t%s\t.\t%s" % (edge[0],edge[1],GC.d_or_u))
        f = open(expanduser("%s/contact_network.txt" % GC.out_dir),'w')
        f.write('\n'.join(out))
        f.close()
        return out