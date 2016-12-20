#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where each transmission occurs a fixed time
delta after the previous transmission
'''
from TransmissionTimeSample import TransmissionTimeSample # abstract TransmissionTimeSample class
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_Fixed(TransmissionTimeSample):
    '''
    Implement the ``TransmissionTimeSample'' with a fixed time delta
    '''

    def sample_time():
        return GC.time + GC.fixed_transmission_time_delta