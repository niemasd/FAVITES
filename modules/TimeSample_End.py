#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TimeSample" module, where the end time is returned for nodes who are infected
at the end time, and no sample times are returned for all other nodes
'''
from TimeSample import TimeSample
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF

class TimeSample_End(TimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "NumTimeSample_Once" in str(MF.modules['NumTimeSample']), "Must use NumTimeSample_Once module"

    def sample_times(node, num_times):
        if node.is_infected():
            return [GC.time]
        else:
            return []