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
        GC.tree_rate_mean = float(GC.tree_rate_mean)
        GC.tree_rate_stdev = float(GC.tree_rate_stdev)
        assert GC.tree_rate_stdev > 0, "tree_rate_stdev must be positive"

    def time_to_mutation_rate(tree):
        parts = tree.split(':')
        for i in range(1,len(parts)):
            try: # branch length is just before a comma
                ind = parts[i].index(',')
                parts[i] = "%f%s" % (float(parts[i][:ind])*lognormal(mean=GC.tree_rate_mean,sigma=GC.tree_rate_stdev), parts[i][ind:])
            except ValueError: # branch length is just before a right parenthesis
                try:
                    ind = parts[i].index(')')
                    parts[i] = "%f%s" % (float(parts[i][:ind])*lognormal(mean=GC.tree_rate_mean,sigma=GC.tree_rate_stdev), parts[i][ind:])
                except ValueError: # branch length is just before the semicolon (root)
                    try:
                        ind = parts[i].index(';')
                        parts[i] = "%f%s" % (float(parts[i][:ind])*lognormal(mean=GC.tree_rate_mean,sigma=GC.tree_rate_stdev), parts[i][ind:])
                    except:
                        assert False, "Failed to parse branch length from tree substring: %s" % parts[i]
        return ':'.join(parts)