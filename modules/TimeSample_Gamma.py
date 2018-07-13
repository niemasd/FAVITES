#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TimeSample" module, where a given node's sample times are randomly from a
Gamma distribution between the window(s) of the node's infection times
'''
from TimeSample import TimeSample
import FAVITES_GlobalContext as GC
from random import choice

class TimeSample_Gamma(TimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.ts_gamma_shape = float(GC.ts_gamma_shape)
        assert GC.ts_gamma_shape > 0, "ts_gamma_shape must be positive"
        GC.ts_gamma_scale = float(GC.ts_gamma_scale)
        assert GC.ts_gamma_scale > 0, "ts_gamma_scale must be positive"
        try:
            global gamma
            from numpy.random import gamma
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading NumPy. Install with: pip3 install numpy"

    def sample_times(node, num_times):
        if not hasattr(GC,"NUMPY_SEEDED"):
            from numpy.random import seed as numpy_seed
            numpy_seed(seed=GC.random_number_seed)
            GC.random_number_seed += 1
            GC.NUMPY_SEEDED = True
        assert hasattr(GC,'transmissions'), "No transmission network found in global context! Run this after the transmission network simulation is done"
        first_time = node.get_first_infection_time()
        if first_time is None:
            return []
        windows = []
        last_time = first_time
        for u,v,t in GC.transmissions:
            if u == node and v == node:
                if last_time is not None and t > last_time:
                    windows.append((last_time,t))
                last_time = None
            elif last_time is None and v == node:
                last_time = t
        if last_time is not None and t > last_time:
            windows.append((last_time, GC.time))
        if len(windows) == 0:
            windows.append((first_time, GC.time))
        out = []
        for i in range(num_times):
            start,end = choice(windows); length = end-start
            delta = float('inf')
            while delta > length:
                delta = gamma(GC.ts_gamma_shape, scale=GC.ts_gamma_scale)
            out.append(delta+start)
        return out