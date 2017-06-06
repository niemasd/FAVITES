#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumBranchSample" module, where a single viral branch is sampled in a given
sampling event
'''
from NumBranchSample import NumBranchSample
import FAVITES_GlobalContext as GC

class NumBranchSample_Single(NumBranchSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def sample_num_branches(node, time):
        return 1