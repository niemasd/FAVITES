#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where each transmission occurs at the present
global time
'''
from TransmissionTimeSample import TransmissionTimeSample
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_Instant(TransmissionTimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def sample_time():
        return GC.time