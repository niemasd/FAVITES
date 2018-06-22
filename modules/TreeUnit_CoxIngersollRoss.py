#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where the mutation rates of branches are determined by a
Cox-Ingersoll-Ross process.
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC
from math import exp

# helper functions for parameterizing Noncentral Chi-Squared with CIR process
def df(a,b,sigma):
    return (4*a*b)/(sigma**2)
def nonc(b,sigma,r0,t):
    return (4*b*r0*exp(-1*b*t))/((sigma**2)*(1-exp(-1*b*t)))

class TreeUnit_CoxIngersollRoss(TreeUnit):
    def cite():
        return [GC.CITATION_FAVITES, GC.CITATION_NUMPY, GC.CITATION_TREESWIFT]

    def init():
        try:
            global noncentral_chisquare
            from numpy.random import noncentral_chisquare
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
        GC.tree_rate_a = float(GC.tree_rate_a)
        assert GC.tree_rate_a > 0, "tree_rate_a must be positive"
        GC.tree_rate_b = float(GC.tree_rate_b)
        assert GC.tree_rate_b > 0, "tree_rate_b must be positive"
        GC.tree_rate_sigma = float(GC.tree_rate_sigma)
        assert GC.tree_rate_sigma > 0, "tree_rate_sigma must be positive"
        GC.tree_rate_R0 = float(GC.tree_rate_R0)
        assert GC.tree_rate_R0 > 0, "tree_rate_R0 must be positive"
        GC.tree_rate_df = df(GC.tree_rate_a,GC.tree_rate_b,GC.tree_rate_sigma)

    def time_to_mutation_rate(tree):
        if not hasattr(GC,"NUMPY_SEEDED"):
            from numpy.random import seed as numpy_seed
            numpy_seed(seed=GC.random_number_seed)
            GC.random_number_seed += 1
            GC.NUMPY_SEEDED = True
        t = read_tree_newick(tree)
        for node in t.traverse_preorder():
            if node.edge_length is None:
                if node.is_root():
                    node.rate = GC.tree_rate_R0
                else:
                    node.rate = node.parent.rate
            else:
                if node.is_root():
                    parent_rate = GC.tree_rate_R0
                else:
                    parent_rate = node.parent.rate
                node.rate = noncentral_chisquare(df=GC.tree_rate_df, nonc=nonc(GC.tree_rate_b,GC.tree_rate_sigma,parent_rate,node.edge_length))
                node.edge_length *= node.rate
        return str(t)
