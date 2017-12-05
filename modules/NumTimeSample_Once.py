#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumTimeSample" module, where each infected node is sampled exactly once
'''
from NumTimeSample import NumTimeSample
import FAVITES_GlobalContext as GC

class NumTimeSample_Once(NumTimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def sample_num_times(node):
        if node.get_first_infection_time() is not None and node.get_first_infection_time() != GC.time:
            return 1
        else:
            return 0