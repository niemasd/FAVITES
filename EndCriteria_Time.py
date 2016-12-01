#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, with a stopping criterion of end time
'''
import FAVITES_Global               # for global access variables
from EndCriteria import EndCriteria # abstract EndCriteria class

class EndCriteria_Time(EndCriteria):
    def done():
        assert FAVITES_Global.end_time is not None, "end_time was never set!"
        return FAVITES_Global.time >= FAVITES_Global.end_time

    def not_done():
        return not EndCriteria_Time.done()