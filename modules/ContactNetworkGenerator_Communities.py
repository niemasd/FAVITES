#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where a ContactNetworkGenerator is specified
for each community, and each possible cross-community edge occurs with
probability p.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from copy import deepcopy
from gzip import open as gopen
from os.path import expanduser
from random import choice,sample,shuffle

class ContactNetworkGenerator_Communities(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_NETWORKX

    def init():
        try:
            global binomial
            from numpy.random import binomial
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NumPy. Install with: pip3 install numpy"
        GC.cn_p_across = float(GC.cn_p_across)
        assert GC.cn_p_across >= 0 and GC.cn_p_across <= 1, "cn_p_across must be between 0 and 1"
        assert isinstance(GC.cn_generators, list), "cn_generators must be a list of dictionaries"
        assert len(GC.cn_generators) != 0, "cn_generators must have at least one community"
        for cng_i, cng in enumerate(GC.cn_generators):
            assert isinstance(cng, dict), "cn_generators must be a list of dictionaries"
            assert 'ContactNetworkGenerator' in cng, 'Each cn_generators dictionary must have a key "ContactNetworkGenerator"'
            assert cng['ContactNetworkGenerator'] in MF.module_implementations['ContactNetworkGenerator'], "%r is not a valid ContactNetworkGenerator!" % cng['ContactNetworkGenerator']
            for param in MF.module_implementations['ContactNetworkGenerator'][cng['ContactNetworkGenerator']]['req']:
                assert param in cng, "Parameter %s missing for ContactNetworkGenerator %d" % (param,cng_i)

    def get_edge_list():
        if hasattr(GC,"cng_community_num"):
            GC.cng_community_num += 1
        else:
            GC.cng_community_num = 0
        local_cn_generators = deepcopy(GC.cn_generators)
        edgelists = []
        for cng_i, cng in enumerate(local_cn_generators):
            MF.modules['ContactNetworkGenerator'] = MF.module_implementations['ContactNetworkGenerator'][cng['ContactNetworkGenerator']]['class']
            for param in MF.module_implementations['ContactNetworkGenerator'][cng['ContactNetworkGenerator']]['req']:
                setattr(GC,param,cng[param])
            MF.modules['ContactNetworkGenerator'].init()
            edgelists.append(MF.modules['ContactNetworkGenerator'].get_edge_list())
        g = {} # g[node]['attributes' or 'edges']
        GC.cn_communities = []
        total_num_nodes = 0
        out = []
        for edgelist_i,edgelist in enumerate(edgelists):
            GC.cn_communities.append([])
            node_prefix = "CNG%d-COM%d"%(GC.cng_community_num,edgelist_i)
            for line in edgelist:
                if len(line) == 0 or line[0] == '#':
                    continue
                parts = line.split()
                assert parts[0] in {'NODE','EDGE'}, "Invalid FAVITES edge list encountered"
                if parts[0] == 'NODE':
                    name = "%s-%s" % (node_prefix,parts[1])
                    assert name not in g, "Duplicate node name encountered"
                    g[name] = {'edges':[], 'attributes':parts[2]}
                    out.append("NODE\t%s\t%s" % (name,parts[2]))
                    GC.cn_communities[-1].append(name)
                else:
                    u = "%s-%s" % (node_prefix,parts[1])
                    assert u in g, "Encountered non-existant node name"
                    v = "%s-%s" % (node_prefix,parts[2])
                    assert v in g, "Encountered non-existant node name"
                    g[u]['edges'].append((v,parts[3],parts[4]))
            assert len(GC.cn_communities[-1]) != 0, "Encountered empty community"
            total_num_nodes += len(GC.cn_communities[-1])
        for u in g:
            for v,attr,du in g[u]['edges']:
                out.append("EDGE\t%s\t%s\t%s\t%s" % (u,v,attr,du))
        possible_across_edges = 0
        for i in range(len(GC.cn_communities)-1):
            for j in range(i+1,len(GC.cn_communities)):
                possible_across_edges += len(GC.cn_communities[i])*len(GC.cn_communities[j])
        num_across_edges = binomial(possible_across_edges,GC.cn_p_across)
        done = set()
        for _ in range(num_across_edges):
            i,j = sample(range(len(GC.cn_communities)),2)
            u,v = choice(GC.cn_communities[i]),choice(GC.cn_communities[j])
            while (u,v) in done:
                i,j = sample(range(len(GC.cn_communities)),2)
                u,v = choice(GC.cn_communities[i]),choice(GC.cn_communities[j])
            done.add((u,v))
            out.append("EDGE\t%s\t%s\t.\tu" % (u,v))
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        f = gopen(expanduser("%s/contact_network_partitions.txt.gz" % GC.out_dir),'wb',9)
        f.write(str(GC.cn_communities).encode()); f.write(b'\n')
        f.close()
        return out