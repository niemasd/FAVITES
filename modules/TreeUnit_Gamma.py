#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where each branch's length (in time units) is multiplied by
a rate that is sampled from a user-parameterized Gamma distribution.
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC

class TreeUnit_Gamma(TreeUnit):
    def cite():
        return GC.CITATION_NUMPY

    def init():
        try:
            global gamma
            from numpy.random import gamma
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NumPy. Install with: pip3 install numpy"
        GC.tree_rate_shape = float(GC.tree_rate_shape)
        assert GC.tree_rate_shape > 0, "tree_rate_shape must be positive"
        GC.tree_rate_scale = float(GC.tree_rate_scale)
        assert GC.tree_rate_scale > 0, "tree_rate_scale must be positive"

    def time_to_mutation_rate(tree):
        t = dendropy.Tree.get(data=tree,schema='newick')
        for edge in t.preorder_edge_iter():
            if edge is not None:
                edge.length *= gamma(shape=GC.tree_rate_shape,scale=GC.tree_rate_scale)
        return str(t) + ';'
