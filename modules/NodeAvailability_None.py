#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeAvailability" module, perfect sampling
'''
from NodeAvailability import NodeAvailability
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF

class NodeAvailability_None(NodeAvailability):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "NumTimeSample_None" in str(MF.modules['NumTimeSample']), "Must use NumTimeSample_None module"
        assert "TimeSample_None" in str(MF.modules['TimeSample']), "Must use TimeSample_None module"

    def subsample_transmission_network():
        return set()