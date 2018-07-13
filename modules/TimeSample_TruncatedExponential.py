#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TimeSample" module, where a given node's sample times are randomly from a
Truncated Exponential distribution across the window of the node's infection
time. If the node has multiple infection times (i.e., from recovery and
reinfection), one window is randomly selected (with uniform probability) for
each sampling.
'''
from TimeSample import TimeSample
import FAVITES_GlobalContext as GC
from random import choice

class TimeSample_TruncatedExponential(TimeSample):
    def cite():
        return GC.CITATION_SCIPY

    def init():
        try:
            global truncexpon
            from scipy.stats import truncexpon
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading SciPy. Install with: pip3 install scipy"

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
        truncexpon_variates = (truncexpon.rvs(1,size=num_times))
        out = []
        for i in range(num_times):
            start,end = choice(windows)
            out.append((truncexpon_variates[i]*(end-start))+start)
        return out