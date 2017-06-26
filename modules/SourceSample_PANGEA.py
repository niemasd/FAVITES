#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SourceSample" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from SourceSample import SourceSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class SourceSample_PANGEA(SourceSample):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.pangea_module_check()

    def sample_virus(node):
        pass