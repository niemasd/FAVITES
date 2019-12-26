#! /usr/bin/env python3
'''
Niema Moshiri 2019

"TransmissionTimeSample" module, where the epidemic is simulated using EpiModel
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_EpiModel(TransmissionTimeSample):
    def cite():
        return GC.CITATION_EPIMODEL

    def init():
        assert "ContactNetworkGenerator_EpiModel" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_EpiModel module"
        assert "EndCriteria_EpiModel" in str(MF.modules['EndCriteria']), "Must use EndCriteria_EpiModel module"
        assert "SeedSelection_EpiModel" in str(MF.modules['SeedSelection']), "Must use SeedSelection_EpiModel module"
        assert "TransmissionNodeSample_EpiModel" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_EpiModel module"

    def sample_time():
        return TransmissionTimeSample_TransmissionFile.sample_time()