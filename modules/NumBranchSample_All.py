#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumBranchSample" module, where all branches at the given time are sampled
'''
from NumBranchSample import NumBranchSample
import modules.FAVITES_ModuleFactory as MF

class NumBranchSample_All(NumBranchSample):
    def init():
        pass

    def sample_num_branches(node, time):
        return float('inf')