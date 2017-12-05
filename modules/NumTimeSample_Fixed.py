#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumTimeSample" module, where each infected individual in the contact network is
sampled a fixed user-specified number of times.
'''
from NumTimeSample import NumTimeSample
import FAVITES_GlobalContext as GC

class NumTimeSample_Fixed(NumTimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.num_sample_times_per_individual = int(GC.num_sample_times_per_individual)
        assert GC.num_sample_times_per_individual > 0, "num_sample_times_per_individual must be a positive integer"

    def sample_num_times(node):
        if node.get_first_infection_time() is not None and node.get_first_infection_time() != GC.time:
            return GC.num_sample_times_per_individual
        else:
            return 0