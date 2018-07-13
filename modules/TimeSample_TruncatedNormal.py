#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TimeSample" module, where a given node's sample times are randomly from a
Truncated Normal distribution across the window of the node's infection time.
If the node has multiple infection times (i.e., from recovery and reinfection),
one window is randomly selected (with uniform probability) for each sampling.

When parameterizing, for the sake of consistency of user-specified parameters,
the time window is fixed as [a,b] = [0,1]. The "ts_truncnorm_loc"
parameter sets the mode of the Truncated Normal distribution, and the
"ts_truncnorm_scale" parameter sets the scale of the Truncated Normal
Distribution. Larger scale = more of the tails included in the window.
'''
from TimeSample import TimeSample
import FAVITES_GlobalContext as GC
from random import choice

class TimeSample_TruncatedNormal(TimeSample):
    def cite():
        return GC.CITATION_SCIPY

    def init():
        GC.ts_truncnorm_loc = float(GC.ts_truncnorm_loc)
        assert GC.ts_truncnorm_loc >= 0 and GC.ts_truncnorm_loc <= 1, "ts_truncnorm_loc must be in the range [0,1]"
        GC.ts_truncnorm_scale = float(GC.ts_truncnorm_scale)
        assert GC.ts_truncnorm_scale > 0, "ts_truncnorm_scale must be positive"
        try:
            global truncnorm
            from scipy.stats import truncnorm
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
        loc = (GC.ts_truncnorm_loc-0.5)*GC.ts_truncnorm_scale
        scale = 1.
        a = (-0.5 + (0.5-GC.ts_truncnorm_loc))*GC.ts_truncnorm_scale
        b = (0.5 + (0.5-GC.ts_truncnorm_loc))*GC.ts_truncnorm_scale
        truncnorm_variates = (truncnorm.rvs(a,b,loc=loc,scale=scale,size=num_times)/GC.ts_truncnorm_scale)+0.5
        out = []
        for i in range(num_times):
            start,end = choice(windows)
            out.append((truncnorm_variates[i]*(end-start))+start)
        return out