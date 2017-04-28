#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, where simulations end immediately (i.e., no transmissions)

This is intended to be used if you only want to simulate a contact network and
nothing else
'''
from EndCriteria import EndCriteria
import modules.FAVITES_ModuleFactory as MF

class EndCriteria_Instant(EndCriteria):
    def init():
        pass

    def done():
        return True

    def not_done():
        return False

    def finalize_time():
        pass