#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumTimeSample" module, where each infected individual in the contact network is
sampled a number of times that is sampled from a Poisson distribution.
'''
from NumTimeSample import NumTimeSample
import FAVITES_GlobalContext as GC

class NumTimeSample_Poisson(NumTimeSample):
    def cite():
        return GC.CITATION_NUMPY

    def init():
        try:
            global poisson
            from numpy.random import poisson
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NumPy. Install with: pip3 install numpy"
        GC.num_time_sample_lambda = float(GC.num_time_sample_lambda)
        assert GC.num_time_sample_lambda >= 0, "num_time_sample_lambda must be at least 0"

    def sample_num_times(node):
        if node.get_first_infection_time() is not None:
            return poisson(lam=GC.num_time_sample_lambda)
        else:
            return 0