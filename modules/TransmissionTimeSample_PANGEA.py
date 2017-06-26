#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from TransmissionTimeSample import TransmissionTimeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_PANGEA(TransmissionTimeSample):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.pangea_module_check()

    def sample_time():
        pass