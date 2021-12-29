#! /usr/bin/env python3
'''
Niema Moshiri 2019

"EndCriteria" module, where the epidemic is simulated using EpiModel
'''
from EndCriteria import EndCriteria
from EndCriteria_TransmissionFile import EndCriteria_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class EndCriteria_EpiModel(EndCriteria):
    def cite():
        return GC.CITATION_EPIMODEL

    def init():
        assert "ContactNetworkGenerator_EpiModel" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_EpiModel module"
        assert "SeedSelection_EpiModel" in str(MF.modules['SeedSelection']), "Must use SeedSelection_EpiModel module"
        assert "TransmissionNodeSample_EpiModel" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_EpiModel module"
        assert "TransmissionTimeSample_EpiModel" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_EpiModel module"

    def done():
        return EndCriteria_TransmissionFile.done()

    def not_done():
        return EndCriteria_TransmissionFile.not_done()

    def finalize_time():
        GC.time = GC.transmission_file[-1][2]
        GC.end_time = GC.transmission_file[-1][2]