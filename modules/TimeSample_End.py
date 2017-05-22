#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TimeSample" module, where the end time is returned for nodes who are infected
at the end time, and no sample times are returned for all other nodes
'''
from TimeSample import TimeSample
import FAVITES_GlobalContext as GC

class TimeSample_End(TimeSample):
    def init():
        pass

    def sample_times(node, num_times):
        if node.is_infected():
            return [GC.time]
        else:
            return []