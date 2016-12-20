#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, with a stopping criterion of end time or number of
transmission events (whichever comes first)
'''
from EndCriteria import EndCriteria                             # abstract EndCriteria class
from EndCriteria_Time import EndCriteria_Time                   # to reuse code
from EndCriteria_Transmissions import EndCriteria_Transmissions # to reuse code

class EndCriteria_FirstTimeTransmissions(EndCriteria):
    def done():
        return EndCriteria_Time.done() or EndCriteria_Transmissions.done()

    def not_done():
        return not EndCriteria_FirstTimeTransmissions.done()

    def finalize_time():
        pass