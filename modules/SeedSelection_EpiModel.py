#! /usr/bin/env python3
'''
Niema Moshiri 2019

"SeedSelection" module, where the epidemic is simulated using EpiModel
'''
from SeedSelection import SeedSelection
from SeedSelection_TransmissionFile import SeedSelection_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class SeedSelection_EpiModel(SeedSelection):
    def cite():
        return GC.CITATION_EPIMODEL

    def init():
        assert "ContactNetworkGenerator_EpiModel" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_EpiModel module"
        assert "EndCriteria_EpiModel" in str(MF.modules['EndCriteria']), "Must use EndCriteria_EpiModel module"
        assert "TransmissionNodeSample_EpiModel" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_EpiModel module"
        assert "TransmissionTimeSample_EpiModel" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_EpiModel module"
        GC.transmission_num = 0

    def select_seeds():
        return SeedSelection_TransmissionFile.select_seeds()