#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where the mutation rate is constant across the entirety of
all trees (i.e., just multiply branch length by mutation rate).
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC

class TreeUnit_ConstantRate(TreeUnit):
    def cite():
        return [GC.CITATION_FAVITES, GC.CITATION_TREESWIFT]

    def init():
        try:
            global read_tree_newick
            from treeswift import read_tree_newick
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading TreeSwift. Install with: pip3 install treeswift"
        GC.tree_mutation_rate = float(GC.tree_mutation_rate)
        assert GC.tree_mutation_rate > 0, "tree_mutation_rate must be positive"

    def time_to_mutation_rate(tree):
        t = read_tree_newick(tree)
        for node in t.traverse_preorder():
            if node.edge_length is not None:
               node.edge_length *= GC.tree_mutation_rate
        return str(t)
