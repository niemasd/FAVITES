#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the graph that is generated is a
Random Partition Graph.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from gzip import open as gopen
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
        assert isinstance(GC.rpg_sizes, list), "rpg_sizes must be a list of positive integers"
        for e in GC.rpg_sizes:
            assert isinstance(e, int) and e > 0, "rpg_sizes must be a list of positive integers"
        assert GC.rpg_p_in >= 0 and GC.rpg_p_in <= 1, "rpg_p_in must be between 0 and 1"
        assert GC.rpg_p_out >= 0 and GC.rpg_p_in <= 1, "rpg_p_in must be between 0 and 1"
        GC.d_or_u = GC.d_or_u.strip()
        assert GC.d_or_u == 'd' or GC.d_or_u == 'u', '"d_or_u" must be either "d" or "u"'

    def get_edge_list():
        du = GC.d_or_u == 'd'
        cn = random_partition_graph(GC.rpg_sizes, GC.rpg_p_in, GC.rpg_p_out, directed=du, seed=GC.random_number_seed)
        if GC.random_number_seed is not None:
            GC.random_number_seed += 1
        out = GC.nx2favites(cn, GC.d_or_u)
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        f = gopen(expanduser("%s/contact_network_partitions.txt.gz" % GC.out_dir),'wb',9)
        f.write(str(cn.graph['partition']).encode()); f.write(b'\n')
        f.close()
        GC.cn_communities = [{str(n) for n in c} for c in cn.graph['partition']]
        return out