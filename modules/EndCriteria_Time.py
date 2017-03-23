#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, with a stopping criterion of end time
'''
from EndCriteria import EndCriteria
import FAVITES_GlobalContext as GC

class EndCriteria_Time(EndCriteria):
    def init():
        GC.end_time = float(GC.end_time)
        assert GC.end_time >= 0, "end_time must be at least 0"

    def done():
        return GC.time >= GC.end_time

    def not_done():
        return not EndCriteria_Time.done()

    def finalize_time():
        GC.time = GC.end_time