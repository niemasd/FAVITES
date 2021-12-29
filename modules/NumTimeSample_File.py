#! /usr/bin/env python3
'''
Niema Moshiri 2020

"NumTimeSample" module, where sample events are read from a file
'''
from NumTimeSample import NumTimeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from os.path import expanduser

class NumTimeSample_File(NumTimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "TimeSample_File" in str(MF.modules['TimeSample']), "Must use TimeSample_File module"
        if GC.sample_time_file.lower().endswith('.gz'):
            from gzip import open as gopen
            GC.sample_times_lines = [i.decode().strip().split() for i in gopen(expanduser(GC.sample_time_file)) if len(i.strip()) > 0 and i[0] != '#']
        else:
            GC.sample_times_lines = [i.strip().split() for i in open(expanduser(GC.sample_time_file)) if len(i.strip()) > 0 and i[0] != '#']
        GC.sample_times_from_file = dict()
        for u,t in GC.sample_times_lines:
            if u not in GC.sample_times_from_file:
                GC.sample_times_from_file[u] = list()
            GC.sample_times_from_file[u].append(float(t))

    def sample_num_times(node):
        u = node.get_name()
        if u in GC.sample_times_from_file:
            return len(GC.sample_times_from_file[u])
        else:
            return 0
