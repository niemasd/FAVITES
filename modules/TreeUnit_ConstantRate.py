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
        return GC.CITATION_NUMPY

    def init():
        GC.tree_mutation_rate = float(GC.tree_mutation_rate)
        assert GC.tree_mutation_rate > 0, "tree_mutation_rate must be positive"

    def time_to_mutation_rate(tree):
        parts = tree.split(':')
        for i in range(1,len(parts)):
            try: # branch length is just before a comma
                ind = parts[i].index(',')
                parts[i] = "%f%s" % (float(parts[i][:ind])*GC.tree_mutation_rate, parts[i][ind:])
            except ValueError: # branch length is just before a right parenthesis
                try:
                    ind = parts[i].index(')')
                    parts[i] = "%f%s" % (float(parts[i][:ind])*GC.tree_mutation_rate, parts[i][ind:])
                except ValueError: # branch length is just before the semicolon (root)
                    try:
                        ind = parts[i].index(';')
                        parts[i] = "%f%s" % (float(parts[i][:ind])*GC.tree_mutation_rate, parts[i][ind:])
                    except:
                        assert False, "Failed to parse branch length from tree substring: %s" % parts[i]
        return ':'.join(parts)