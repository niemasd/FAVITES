#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, with a stopping criterion of end time or number of
transmission events (whichever comes first)
'''
from modules import FAVITES_Global                                      # for global access variables
from modules.EndCriteria import EndCriteria                             # abstract EndCriteria class
from modules.EndCriteria_Time import EndCriteria_Time                   # to reuse code
from modules.EndCriteria_Transmissions import EndCriteria_Transmissions # to reuse code

class EndCriteria_FirstTimeTransmissions(EndCriteria):
    def __init__(self):
        EndCriteria_Time()          # check for validity
        EndCriteria_Transmissions() # check for validity

    def done():
        return EndCriteria_Time.done() or EndCriteria_Transmissions.done()

    def not_done():
        return not EndCriteria_FirstTimeTransmissions.done()