#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumTimeSample" module, where no nodes are sampled
'''
from NumTimeSample import NumTimeSample
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF

class NumTimeSample_None(NumTimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "NodeAvailability_None" in str(MF.modules['NodeAvailability']), "Must use NodeAvailability_None module"
        assert "TimeSample_None" in str(MF.modules['TimeSample']), "Must use TimeSample_None module"

    def sample_num_times(node):
        return 0