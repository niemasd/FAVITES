#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from NodeEvolution import NodeEvolution
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class NodeEvolution_PANGEA(NodeEvolution):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.pangea_module_check()

    def evolve_to_current_time(node, finalize=False):
        pass