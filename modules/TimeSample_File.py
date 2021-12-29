#! /usr/bin/env python3
'''
Niema Moshiri 2020

"TimeSample" module, where sample events are read from a file
'''
from TimeSample import TimeSample
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF

class TimeSample_File(TimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "NumTimeSample_File" in str(MF.modules['NumTimeSample']), "Must use NumTimeSample_File module"
        # NumTimeSample_File sets everything up

    def sample_times(node, num_times):
        if num_times == 0:
            return list()
        else:
            return GC.sample_times_from_file[node.get_name()]
