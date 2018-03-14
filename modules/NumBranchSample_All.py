#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumBranchSample" module, where all branches at the given time are sampled
'''
from NumBranchSample import NumBranchSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class NumBranchSample_All(NumBranchSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "VirusTreeSimulator" not in str(MF.modules['NodeEvolution']), "Cannot use a coalescent model of evolution with NumBranchSample_All"

    def sample_num_branches(node, time):
        return float('inf')