#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, with a stopping criterion of number of transmission events
'''
from EndCriteria import EndCriteria # abstract EndCriteria class
import FAVITES_GlobalContext as GC

class EndCriteria_Transmissions(EndCriteria):
    def done():
        assert GC.end_transmissions >= 0, "end_transmissions is negative!"
        assert GC.contact_network is not None, "contact_network was never set!"
        return GC.contact_network.num_transmissions() >= GC.end_transmissions

    def not_done():
        return not EndCriteria_Transmissions.done()

    def finalize_time():
        pass