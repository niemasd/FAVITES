#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented with the Yule model
'''
from NodeEvolution import NodeEvolution # abstract NodeEvolution class
from NodeEvolution_DualBirth import NodeEvolution_DualBirth
import FAVITES_GlobalContext as GC

class NodeEvolution_Yule(NodeEvolution):
    def init():
        GC.rate_A = float(GC.yule_rate)
        GC.rate_B = float(GC.yule_rate)

    def evolve_to_current_time(node, finalize=False):
        NodeEvolution_DualBirth.evolve_to_current_time(node, finalize=finalize)