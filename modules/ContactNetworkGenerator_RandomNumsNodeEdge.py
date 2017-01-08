#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where a user-specified number of nodes are
created, and a user-specified number of edges are randomly placed on the graph
'''
from ContactNetworkGenerator import ContactNetworkGenerator # abstract ContactNetworkGenerator class
import FAVITES_GlobalContext as GC
from os import path
from random import sample

class ContactNetworkGenerator_RandomNumsNodeEdge(ContactNetworkGenerator):
    '''
    Implement the ``ContactNetworkGenerator'', loading the edge list from file
    '''

    def init():
        GC.num_cn_nodes = int(GC.num_cn_nodes)
        GC.num_cn_edges = int(GC.num_cn_edges)
        if GC.num_cn_nodes < 2:
            print("ERROR: Contact network must have more than >= 2 nodes")
            exit(-1)
        if GC.num_cn_edges > GC.num_cn_nodes * (GC.num_cn_nodes - 1):
            print("ERROR: If there are n contact network nodes, there cannot be more than n*(n-1) edges")
            exit(-1)

    def get_edge_list():
        nodes = [str(i) for i in range(GC.num_cn_nodes)]
        out = ["NODE\t" + node + "\t." for node in nodes]
        poss_edges = set([(u,v) for u in nodes for v in nodes if u != v])
        for _ in range(GC.num_cn_edges):
            edge = sample(poss_edges,1)[0]
            poss_edges.remove(edge)
            out.append("EDGE\t" + edge[0] + "\t" + edge[1] + "\t.\td")
        f = open(path.expanduser(GC.out_dir + "/contact_network.txt"),'w')
        f.write('\n'.join(out))
        f.close()
        return out