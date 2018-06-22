#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where each branch's length (in time units) is multiplied by
a rate that is sampled from a Gamma distribution whose mean is the rate of the
parent branch and whose variance is the branch length multiplied by a
user-specified constant v.

shape*scale = node.parent.rate and shape*scale^2 = v*node.edge_length
shape = node.parent.rate/scale, so (node.parent.rate/scale)*scale^2 = v*node.edge_length
node.parent.rate*scale = v*node.edge_length, therefore:

scale = v * node.edge_length / node.parent.rate
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC

class TreeUnit_AutocorrelatedGamma(TreeUnit):
    def cite():
        return [GC.CITATION_FAVITES, GC.CITATION_NUMPY, GC.CITATION_TREESWIFT]

    def init():
        try:
            global gamma
            from numpy.random import gamma
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NumPy. Install with: pip3 install numpy"
        try:
            global read_tree_newick
            from treeswift import read_tree_newick
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading TreeSwift. Install with: pip3 install treeswift"
        GC.tree_rate_v = float(GC.tree_rate_v)
        assert GC.tree_rate_v > 0, "tree_rate_v must be positive"
        GC.tree_rate_R0 = float(GC.tree_rate_R0)
        assert GC.tree_rate_R0 > 0, "tree_rate_R0 must be positive"

    def time_to_mutation_rate(tree):
        if not hasattr(GC,"NUMPY_SEEDED"):
            from numpy.random import seed as numpy_seed
            numpy_seed(seed=GC.random_number_seed)
            GC.random_number_seed += 1
            GC.NUMPY_SEEDED = True
        t = read_tree_newick(tree)
        for node in t.traverse_preorder():
            if node.is_root():
                node.rate = GC.tree_rate_R0
            else:
                assert node.edge_length is not None and node.edge_length > 0, "All edges must have positive lengths for TreeUnit_AutocorrelatedGamma"
                scale = GC.tree_rate_v * node.edge_length / node.parent.rate
                shape = node.parent.rate / scale
                node.rate = gamma(shape=shape,scale=scale)
            if node.edge_length is not None: # root node might not have incident edge
                node.edge_length *= node.rate
        return str(t)
