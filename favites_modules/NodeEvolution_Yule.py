#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented with the Yule model
'''
from NodeEvolution import NodeEvolution
from NodeEvolution_DualBirth import NodeEvolution_DualBirth
import FAVITES_GlobalContext as GC

class NodeEvolution_Yule(NodeEvolution):
    def init():
        GC.rate_A = float(GC.yule_rate)
        GC.rate_B = float(GC.yule_rate)
        GC.dualbirth_beta = 1/(float(GC.rate_B))
        GC.dualbirth_betaP = 1/(float(GC.rate_A))
        NodeEvolution_DualBirth.init()

    def evolve_to_current_time(node, finalize=False):
        NodeEvolution_DualBirth.evolve_to_current_time(node, finalize=finalize)