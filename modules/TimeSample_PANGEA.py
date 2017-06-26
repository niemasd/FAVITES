#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TimeSample" module, where the end time is returned for nodes who are infected
at the end time, and no sample times are returned for all other nodes
'''
from TimeSample import TimeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TimeSample_PANGEA(TimeSample):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.pangea_module_check()

    def sample_times(node, num_times):
        return []