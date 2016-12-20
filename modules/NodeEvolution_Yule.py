#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented with the Yule model
'''
from NodeEvolution import NodeEvolution # abstract NodeEvolution class
from NodeEvolution_DualBirth import NodeEvolution_DualBirth
import FAVITES_GlobalContext as GC

class NodeEvolution_Yule(NodeEvolution):
    def evolve_to_current_time(node, finalize=False):
        if not hasattr(GC, "rate_A"):
            GC.rate_A = GC.rate
            GC.rate_B = GC.rate
        NodeEvolution_DualBirth.evolve_to_current_time(node, finalize=finalize)