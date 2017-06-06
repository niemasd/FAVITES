#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumBranchSample" module, where the number of viral branches to be sampled is
a constant user-specified value. If the number of available viral branches is
less than the user-specified value, all viral branches will be sampled.
'''
from NumBranchSample import NumBranchSample
import FAVITES_GlobalContext as GC

class NumBranchSample_Fixed(NumBranchSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        if isinstance(GC.num_viruses_per_cn_sample, str) and len(GC.num_viruses_per_cn_sample.strip()) == 0:
            GC.num_viruses_per_cn_sample = float('inf')
        else:
            GC.num_viruses_per_cn_sample = int(GC.num_viruses_per_cn_sample)
            assert GC.num_viruses_per_cn_sample > 0, "num_viruses_per_cn_sample must be positive"

    def sample_num_branches(node, time):
        return GC.num_viruses_per_cn_sample