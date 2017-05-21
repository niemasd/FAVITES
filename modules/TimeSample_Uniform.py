#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TimeSample" module, where a given node's sample times are randomly from a
uniform distribution between the window(s) of the node's infection times
'''
from TimeSample import TimeSample
import FAVITES_GlobalContext as GC
from random import uniform

class TimeSample_Uniform(TimeSample):
    def init():
        pass

    def sample_times(node):
        assert hasattr(GC,'transmissions'), "No transmission network found in global context! Run this after the transmission network simulation is done"
        first_time = node.get_first_infection_time()
        if first_time is None:
            return []
        windows = []
        last_time = first_time
        for u,v,t in GC.transmissions:
            if u == node and v == node:
                if t > last_time:
                    windows.append((last_time,t))
                last_time = None
            elif last_time is None and v == node:
                last_time = t
        if t > last_time:
            windows.append((last_time, GC.time))
        weighted_die = {}
        for start,end in windows:
            weighted_die[(start,end)] = end-start
        if len(weighted_die) == 0:
            return []
        if len(weighted_die) == 1:
            weighted_die[list(weighted_die.keys())[0]] = 1
        out = []
        for _ in range(GC.num_sample_times):
            start,end = GC.roll(weighted_die)
            out.append(uniform(start,end))
        return out