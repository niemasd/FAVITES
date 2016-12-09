#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, with a stopping criterion of end time
'''
from EndCriteria import EndCriteria # abstract EndCriteria class
import FAVITES_GlobalContext as GC

class EndCriteria_Time(EndCriteria):
    def __init__(self):
        assert GC.end_time != None, "Missing --EndTime argument"

    def done():
        assert GC.end_time >= 0, "end_time is negative!"
        return GC.time >= GC.end_time

    def not_done():
        return not EndCriteria_Time.done()