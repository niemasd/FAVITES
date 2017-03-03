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

    def init():
        global exponential
        from numpy.random import exponential

    def sample_time():
        return GC.time + exponential(scale=1/(float(GC.time_sample_rate)))