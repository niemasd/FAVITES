#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from SeedSelection import SeedSelection
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class SeedSelection_PANGEA(SeedSelection):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.pangea_module_check()

    def select_seeds():
        return []