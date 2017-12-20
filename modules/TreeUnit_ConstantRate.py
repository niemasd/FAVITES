#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where the mutation rate is constant across the entirety of
all trees (i.e., just multiply branch length by mutation rate).
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC
import dendropy

class TreeUnit_ConstantRate(TreeUnit):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        try:
            global dendropy
            import dendropy
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading DendroPy. Install with: pip3 install dendropy"
        GC.tree_mutation_rate = float(GC.tree_mutation_rate)
        assert GC.tree_mutation_rate > 0, "tree_mutation_rate must be positive"

    def time_to_mutation_rate(tree):
        t = dendropy.Tree.get(data=tree,schema='newick')
        for edge in t.preorder_edge_iter():
            if edge.length is not None:
               edge.length *= GC.tree_mutation_rate
        return '%s;' % str(t)
