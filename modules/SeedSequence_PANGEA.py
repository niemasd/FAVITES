#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from SeedSequence import SeedSequence
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class SeedSequence_PANGEA(SeedSequence):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.pangea_module_check()

    def generate():
        return ''

    def merge_trees():
        return [],[]
