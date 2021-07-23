#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented such that there are no speciations or deaths
(the root simply propagates through time). The result is a phylogenetic tree
containing a single leaf.
'''
from NodeEvolution import NodeEvolution
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class NodeEvolution_None(NodeEvolution):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def evolve_to_current_time(node, finalize=False):
        if node is None:
            return
        for virus in node.viruses():
            virus.set_time(GC.time)
