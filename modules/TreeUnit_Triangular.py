#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where each branch's length (in time units) is multiplied by
a rate that is sampled from a user-parameterized Triangular distribution.
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC

class TreeUnit_Triangular(TreeUnit):
    def cite():
        return GC.CITATION_NUMPY

    def init():
        try:
            global triangular
            from numpy.random import triangular
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
        GC.tree_rate_left = float(GC.tree_rate_left)
        GC.tree_rate_mode = float(GC.tree_rate_mode)
        GC.tree_rate_right = float(GC.tree_rate_right)
        assert GC.tree_rate_left <= GC.tree_rate_mode, "tree_rate_left must be <= GC.tree_rate_mode"
        assert GC.tree_rate_mode <= GC.tree_rate_right, "tree_rate_mode must be <= GC.tree_rate_right"

    def time_to_mutation_rate(tree):
        if not hasattr(GC,"NUMPY_SEEDED"):
            from numpy.random import seed as numpy_seed
            numpy_seed(seed=GC.random_number_seed)
            GC.random_number_seed += 1
            GC.NUMPY_SEEDED = True
        t = read_tree_newick(tree)
        for node in t.traverse_preorder():
            if node.edge_length is not None:
                node.edge_length *= triangular(left=GC.tree_rate_left,mode=GC.tree_rate_mode,right=GC.tree_rate_right)
        return str(t)
