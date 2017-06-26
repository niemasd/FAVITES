#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeAvailability" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from NodeAvailability import NodeAvailability
from ContactNetworkNode_PANGEA import ContactNetworkNode_PANGEA as Node
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from glob import glob

class NodeAvailability_PANGEA(NodeAvailability):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.pangea_module_check()

    def subsample_transmission_network():
        out = set()
        for f in glob(GC.out_dir + "/error_free_files/sequence_data/seqs_*"):
            out.add(Node(None,f.split('/')[-1][5:-6],None))
        return out