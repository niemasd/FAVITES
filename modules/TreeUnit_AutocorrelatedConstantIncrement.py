#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where each branch's length (in time units) is multiplied by
a rate. The rate of a given branch is either equal to the rate of its parent
with probability 1-p or is incremented or decremented by delta with probability
p/2. The root edge has rate R0. The rates are bounded above and below by
rate_max and rate_min, respectively.
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC
from random import random

class TreeUnit_AutocorrelatedConstantIncrement(TreeUnit):
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
        GC.tree_rate_p = float(GC.tree_rate_p)
        assert 0 <= GC.tree_rate_p <= 1, "tree_rate_R0 must be positive"
        GC.tree_rate_delta = float(GC.tree_rate_delta)
        assert GC.tree_rate_delta >= 0, "tree_rate_delta must be at least 0"
        GC.tree_rate_R0 = float(GC.tree_rate_R0)
        assert GC.tree_rate_R0 > 0, "tree_rate_R0 must be positive"
        GC.tree_rate_max = float(GC.tree_rate_max)
        assert GC.tree_rate_max >= 0, "tree_rate_max must be at least 0"
        GC.tree_rate_min = float(GC.tree_rate_min)
        assert GC.tree_rate_min >= 0, "tree_rate_min must be at least 0"

    def time_to_mutation_rate(tree):
        t = read_tree_newick(tree)
        for node in t.traverse_preorder():
            if node.is_root():
                node.rate = GC.tree_rate_R0
            else:
                node.rate = node.parent.rate
                r = random()
                if r < GC.tree_rate_p/2: # increment
                    node.rate += GC.tree_rate_delta
                    if node.rate > GC.tree_rate_max:
                        node.rate = GC.tree_rate_max
                elif r < GC.tree_rate_p: # decrement
                    node.rate -= GC.tree_rate_delta
                    if node.rate < GC.tree_rate_min:
                        node.rate = GC.tree_rate_min
            if node.edge_length is not None:
                node.edge_length *= node.rate
        return str(t)
