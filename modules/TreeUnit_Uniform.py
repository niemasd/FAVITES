#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where each branch's length (in time units) is multiplied by
a rate that is sampled from a user-parameterized Uniform distribution.
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC
from random import uniform

class TreeUnit_Uniform(TreeUnit):
    def cite():
        return [GC.CITATION_FAVITES,GC.CITATION_TREESWIFT]

    def init():
        try:
            global read_tree_newick
            from treeswift import read_tree_newick
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading TreeSwift. Install with: pip3 install treeswift"
        GC.tree_rate_min = float(GC.tree_rate_min)
        GC.tree_rate_max = float(GC.tree_rate_max)
        assert GC.tree_rate_min <= GC.tree_rate_max, "tree_rate_min must be <= GC.tree_rate_max"

    def time_to_mutation_rate(tree):
        if not hasattr(GC,"NUMPY_SEEDED"):
            from numpy.random import seed as numpy_seed
            numpy_seed(seed=GC.random_number_seed)
            GC.random_number_seed += 1
            GC.NUMPY_SEEDED = True
        t = read_tree_newick(tree)
        for node in t.traverse_preorder():
            if node.edge_length is not None:
                node.edge_length *= uniform(GC.tree_rate_min,GC.tree_rate_max)
        return str(t)
