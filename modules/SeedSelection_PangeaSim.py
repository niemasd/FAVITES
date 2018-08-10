#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where the transmission network is read from a file

Seed nodes are passed in via the "seed_file" parameter of the configuration file
'''
from SeedSelection import SeedSelection
from SeedSelection_TransmissionFile import SeedSelection_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class SeedSelection_PangeaSim(SeedSelection):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        assert "ContactNetworkGenerator_PangeaSim" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_PangeaSim module"
        assert "EndCriteria_PangeaSim" in str(MF.modules['EndCriteria']), "Must use EndCriteria_PangeaSim module"
        assert "TransmissionNodeSample_PangeaSim" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_PangeaSim module"
        assert "TransmissionTimeSample_PangeaSim" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_PangeaSim module"
        GC.transmission_num = 0

    def select_seeds():
        return SeedSelection_TransmissionFile.select_seeds()