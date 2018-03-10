#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where each transmission occurs a time delta
after the previous, where delta is sampled from an exponential
'''
from TransmissionTimeSample import TransmissionTimeSample
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_Exponential(TransmissionTimeSample):
    '''
    Implement the ``TransmissionTimeSample'' where time deltas are sampled from
    an exponential distribution
    '''

    def cite():
        return GC.CITATION_NUMPY

    def init():
        try:
            global exponential
            from numpy.random import exponential
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading Numpy. Install with: pip3 install numpy"

    def sample_time():
        if not hasattr(GC,"NUMPY_SEEDED"):
            from numpy.random import seed as numpy_seed
            numpy_seed(seed=GC.random_number_seed)
            GC.random_number_seed += 1
            GC.NUMPY_SEEDED = True
        return GC.time + exponential(scale=1/(float(GC.time_sample_rate)))