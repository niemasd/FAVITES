#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, with a stopping criterion of end time or number of
transmission events (whichever comes first)
'''
from EndCriteria import EndCriteria
from EndCriteria_Time import EndCriteria_Time
from EndCriteria_Transmissions import EndCriteria_Transmissions
import FAVITES_GlobalContext as GC

class EndCriteria_FirstTimeTransmissions(EndCriteria):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def done():
        return EndCriteria_Time.done() or EndCriteria_Transmissions.done()

    def not_done():
        return not EndCriteria_FirstTimeTransmissions.done()

    def finalize_time():
        pass