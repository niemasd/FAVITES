#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph that is generated is a
Random Partition Graph.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser

class ContactNetworkGenerator_RandomPartitionGraph(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global random_partition_graph
            from networkx import random_partition_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.rpg_sizes, list), "rpg_sizes must be a list of integers"
        for e in GC.rpg_sizes:
            assert isinstance(e, int), "rpg_sizes must be a list of integers"
        assert GC.rpg_p_in >= 0 and GC.rpg_p_in <= 1, "rpg_p_in must be between 0 and 1"
        assert GC.rpg_p_out >= 0 and GC.rpg_p_in <= 1, "rpg_p_in must be between 0 and 1"

    def get_edge_list():
        cn = random_partition_graph(GC.rpg_sizes, GC.rpg_p_in, GC.rpg_p_out)
        out = GC.nx2favites(cn, 'u')
        f = open(expanduser("%s/contact_network.txt" % GC.out_dir),'w')
        f.write('\n'.join(out))
        f.close()
        return out