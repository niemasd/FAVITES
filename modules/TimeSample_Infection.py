#! /usr/bin/env python3
'''
Niema Moshiri 2020

"TimeSample" module, where individuals are sampled the first time they
are infected.
'''
from TimeSample import TimeSample
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF

class TimeSample_Infection(TimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "NumTimeSample_Once" in str(MF.modules['NumTimeSample']), "Must use NumTimeSample_Once module"

    def sample_times(node, num_times):
        if not hasattr(GC, "inf_time"):
            GC.inf_time = dict()
            for u,v,t in GC.transmissions:
                if v not in GC.inf_time: # only pick first infection time
                    GC.inf_time[v] = t
        if node in GC.inf_time:
            return [GC.inf_time[node]]
        else:
            return list()
