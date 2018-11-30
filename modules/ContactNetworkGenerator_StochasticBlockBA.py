#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the contact network is sampled using
the Stochastic Block Barabasi-Albert model: a BA graph is sampled for each
community independently with different values of m parameter between 1 and
cng_m, and random edges are placed between nodes of different communities with
probability cng_p.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from gzip import open as gopen
from os.path import expanduser
from random import choice

class ContactNetworkGenerator_StochasticBlockBA(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global multinomial; global binomial
            from numpy.random import multinomial,binomial
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NumPy. Install with: pip3 install numpy"
        try:
            global barabasi_albert_graph
            from networkx import barabasi_albert_graph
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NetworkX. Install with: pip3 install networkx"
        assert isinstance(GC.cng_m,int) and GC.cng_m > 0, "cng_m must be a positive integer"
        GC.cng_p = float(GC.cng_p)
        assert 0 <= GC.cng_p <= 1, "cng_p must be between 0 and 1"
        assert isinstance(GC.cng_N,list) and len(GC.cng_N) != 0, "cng_N must be a list of positive integers"
        for n in GC.cng_N:
            assert isinstance(n,int) and n > 0, "cng_N must be a list of positive integers"

    def get_edge_list():
        # set things up
        a = (GC.cng_m+1)/(2*GC.cng_m)
        probs = [0]+[2*a/(i*(i+1)) for i in range(1,GC.cng_m+1)] # prepend 0 to make non-zero probabilities be indices 1 through M
        M = [m for m,n in enumerate(multinomial(len(GC.cng_N), probs, size=1)[0]) for _ in range(n)]
        com = list()
        for i in range(len(M)):
            com.append(GC.nx2favites(barabasi_albert_graph(GC.cng_N[i], M[i], seed=GC.random_number_seed),'u'))
            if GC.random_number_seed is not None:
                GC.random_number_seed += 1

        # process disconnected BA graphs (one per community)
        nodes = list(); node_lines = list(); edge_lines = list(); GC.cn_communities = list()
        for i,g in enumerate(com):
            nodes.append(list()); GC.cn_communities.append(set())
            node_prefix = 'COM%d'%i
            for l in g:
                if len(l) == 0 or l[0] == '#':
                    continue
                parts = l.split()
                assert parts[0] in {'NODE','EDGE'}, "Invalid FAVITES edge list encountered"
                if parts[0] == 'NODE':
                    name = "%s-%s" % (node_prefix,parts[1])
                    nodes[-1].append(name); GC.cn_communities[-1].add(name)
                    node_lines.append("NODE\t%s\t%s" % (name,parts[2]))
                else:
                    u = "%s-%s" % (node_prefix,parts[1])
                    v = "%s-%s" % (node_prefix,parts[2])
                    edge_lines.append("EDGE\t%s\t%s\t%s\t%s" % (u,v,parts[3],parts[4]))

        # add edges between communities
        possible_num_er_edges = sum(len(c) for c in nodes)**2 - sum(len(c)**2 for c in nodes)
        if len(nodes) == 1:
            num_er_edges = 0 # only 1 community
        else:
            num_er_edges = 2*binomial(possible_num_er_edges, GC.cng_p) # multiply by 2 for bidirectionality
        er_edges = set()
        er_choice_indices = list(range(len(nodes)))
        while len(er_edges) != 2*num_er_edges:
            i = choice(er_choice_indices)
            j = choice(er_choice_indices)
            while i == j:
                j = choice(er_choice_indices)
            u = choice(nodes[i]); v = choice(nodes[j])
            er_edges.add((u,v)); er_edges.add((v,u))
            edge_lines.append("EDGE\t%s\t%s\t.\tu" % (u,v))

        # output final graph
        out = node_lines+edge_lines
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        f = gopen(expanduser("%s/contact_network_partitions.txt.gz" % GC.out_dir),'wb',9)
        f.write(str(GC.cn_communities).encode()); f.write(b'\n')
        f.close()
        return out