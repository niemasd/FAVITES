#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from TransmissionNodeSample import TransmissionNodeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionNodeSample_PANGEA(TransmissionNodeSample):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.pangea_module_check()

    def sample_nodes(time):
        return None

    def check_contact_network(cn):
        pass