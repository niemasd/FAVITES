#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module, where no modification is done to the input tree
'''
from TreeUnit import TreeUnit
import FAVITES_GlobalContext as GC

class TreeUnit_Same(TreeUnit):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def time_to_mutation_rate(tree):
        return tree