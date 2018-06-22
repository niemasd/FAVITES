#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where each branch's length (in time units) is multiplied by
a rate that is sampled from a log-normal distribution whose underlying mean
is the rate of the parent branch and whose variance is the branch length
multiplied by a user-specified constant v.
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC

class TreeUnit_AutocorrelatedLogNormal(TreeUnit):
    def cite():
        return [GC.CITATION_FAVITES, GC.CITATION_NUMPY, GC.CITATION_TREESWIFT]

    def init():
        try:
            global lognormal
            from numpy.random import lognormal
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
                assert node.edge_length is not None and node.edge_length > 0, "All edges must have positive lengths for TreeUnit_AutocorrelatedLogNormal"
                node.rate = lognormal(mean=node.parent.rate, sigma=GC.tree_rate_v*node.edge_length)
            if node.edge_length is not None: # root node might not have incident edge
                node.edge_length *= node.rate
        return str(t)
