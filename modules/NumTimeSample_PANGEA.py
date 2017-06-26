#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumTimeSample" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from NumTimeSample import NumTimeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class NumTimeSample_PANGEA(NumTimeSample):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.pangea_module_check()

    def sample_num_times(node):
        return 0