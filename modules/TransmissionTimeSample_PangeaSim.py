#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is read from a
file
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_PangeaSim(TransmissionTimeSample):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        assert "ContactNetworkGenerator_PangeaSim" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_PangeaSim module"
        assert "EndCriteria_PangeaSim" in str(MF.modules['EndCriteria']), "Must use EndCriteria_PangeaSim module"
        assert "SeedSelection_PangeaSim" in str(MF.modules['SeedSelection']), "Must use SeedSelection_PangeaSim module"
        assert "TransmissionNodeSample_PangeaSim" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_PangeaSim module"

    def sample_time():
        return TransmissionTimeSample_TransmissionFile.sample_time()