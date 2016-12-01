#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, with a stopping criterion of number of transmission events
'''
import FAVITES_Global               # for global access variables
from EndCriteria import EndCriteria # abstract EndCriteria class

class EndCriteria_Transmissions(EndCriteria):
    def done():
        assert FAVITES_Global.contact_network is not None, "contact_network was never set!"
        return FAVITES_Global.contact_network.num_transmissions() >= FAVITES_Global.end_transmissions

    def not_done():
        return not EndCriteria_Transmissions.done()