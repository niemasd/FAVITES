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
        return GC.CITATION_NUMPY

    def init():
        try:
            global lognormal
            from numpy.random import lognormal
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NumPy. Install with: pip3 install numpy"
        try:
            global dendropy
            import dendropy
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading DendroPy. Install with: pip3 install dendropy"
        GC.tree_rate_mean = float(GC.tree_rate_mean)
        GC.tree_rate_stdev = float(GC.tree_rate_stdev)
        assert GC.tree_rate_stdev > 0, "tree_rate_stdev must be positive"

    def time_to_mutation_rate(tree):
        t = dendropy.Tree.get(data=tree,schema='newick')
        for edge in t.preorder_edge_iter():
            if edge is not None:
                edge.length *= lognormal(mean=GC.tree_rate_mean,sigma=GC.tree_rate_stdev)
        return str(t) + ';'
