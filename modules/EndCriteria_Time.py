#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, with a stopping criterion of end time
'''
from modules import FAVITES_Global          # for global access variables
from modules.EndCriteria import EndCriteria # abstract EndCriteria class

class EndCriteria_Time(EndCriteria):
    def __init__(self):
        assert FAVITES_Global.end_time != None, "Missing --EndTime argument"

    def done():
        assert FAVITES_Global.end_time >= 0, "end_time is negative!"
        return FAVITES_Global.time >= FAVITES_Global.end_time

    def not_done():
        return not EndCriteria_Time.done()