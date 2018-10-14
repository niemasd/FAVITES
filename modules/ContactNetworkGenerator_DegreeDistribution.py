#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, creating a random graph with a user-defined degree distribution
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from os.path import expanduser

class ContactNetworkGenerator_DegreeDistribution(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global random_degree_sequence_graph
            from networkx import random_degree_sequence_graph
            global NetworkXUnfeasible
            from networkx import NetworkXUnfeasible
            global NetworkXError
            from networkx import NetworkXError
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        if GC.cn_tries == None or GC.cn_tries == '':
            GC.cn_tries = 10 # this is the NetworkX default
        else:
            assert isinstance(GC.cn_tries,int) and GC.cn_tries > 0, "cn_tries must be a positive integer"
        assert isinstance(GC.cn_degree_distribution, dict), "cn_degree_distribution must be a dictionary"
        GC.num_cn_nodes = 0
        for d in GC.cn_degree_distribution:
            assert isinstance(d,int) and d >= 0, "cn_degree_distribution keys must be non-negative integers (degrees)"
            assert isinstance(GC.cn_degree_distribution[d],int) and GC.cn_degree_distribution[d] >= 0, "cn_degree_distribution values must be non-negative integers (counts)"
            GC.num_cn_nodes += GC.cn_degree_distribution[d]
        assert GC.num_cn_nodes >= 2, "Contact network must have at least 2 nodes"
        GC.cn_degree_sequence = [d for d in GC.cn_degree_distribution for _ in range(GC.cn_degree_distribution[d])]

    def get_edge_list():
        try:
            cn = random_degree_sequence_graph(GC.cn_degree_sequence, tries=GC.cn_tries, seed=GC.random_number_seed)
        except NetworkXUnfeasible:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Contact network degree sequence is not graphical"
        except NetworkXError:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "NetworkX failed to produce graph after %d tries" % GC.cn_tries
        if GC.random_number_seed is not None:
            GC.random_number_seed += 1
        out = GC.nx2favites(cn, 'u')
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        return out