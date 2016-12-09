#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where each transmission occurs a fixed time
delta after the previous transmission
'''
from TransmissionTimeSample import TransmissionTimeSample # abstract TransmissionTimeSample class
from ContactNetworkNode import ContactNetworkNode         # to verify u and v
import FAVITES_GlobalContext as GC
from random import sample                                         # to randomly sample seed nodes

class TransmissionTimeSample_Fixed(TransmissionTimeSample):
    '''
    Implement the ``TransmissionTimeSample'' with a fixed time delta
    '''

    def __init__(self):
        assert GC.fixed_transmission_time_delta != None, "Missing --FixedTransmissionTimeDelta argument"

    def sample_time(source,target):
        return GC.time + GC.fixed_transmission_time_delta