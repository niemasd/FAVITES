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
        parts = tree.split(':')
        for i in range(1,len(parts)):
            try: # branch length is just before a comma
                ind = parts[i].index(',')
                parts[i] = "%f%s" % (float(parts[i][:ind])*gamma(shape=GC.tree_rate_shape,scale=GC.tree_rate_scale), parts[i][ind:])
            except ValueError: # branch length is just before a right parenthesis
                try:
                    ind = parts[i].index(')')
                    parts[i] = "%f%s" % (float(parts[i][:ind])*gamma(shape=GC.tree_rate_shape,scale=GC.tree_rate_scale), parts[i][ind:])
                except ValueError: # branch length is just before the semicolon (root)
                    try:
                        ind = parts[i].index(';')
                        parts[i] = "%f%s" % (float(parts[i][:ind])*gamma(shape=GC.tree_rate_shape,scale=GC.tree_rate_scale), parts[i][ind:])
                    except:
                        assert False, "Failed to parse branch length from tree substring: %s" % parts[i]
        return ':'.join(parts)