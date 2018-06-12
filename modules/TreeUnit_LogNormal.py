#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where each branch's length (in time units) is multiplied by
a rate that is sampled from a user-parameterized log-normal distribution.
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC

class TreeUnit_LogNormal(TreeUnit):
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
        GC.tree_rate_mean = float(GC.tree_rate_mean)
        GC.tree_rate_stdev = float(GC.tree_rate_stdev)
        assert GC.tree_rate_stdev > 0, "tree_rate_stdev must be positive"

    def time_to_mutation_rate(tree):
        if not hasattr(GC,"NUMPY_SEEDED"):
            from numpy.random import seed as numpy_seed
            numpy_seed(seed=GC.random_number_seed)
            GC.random_number_seed += 1
            GC.NUMPY_SEEDED = True
        t = read_tree_newick(tree)
        for node in t.traverse_preorder():
            if node.edge_length is not None:
                node.edge_length *= lognormal(mean=GC.tree_rate_mean,sigma=GC.tree_rate_stdev)
        return str(t)
