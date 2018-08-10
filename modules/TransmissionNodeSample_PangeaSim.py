#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module, where the transmission network is read from a
file
'''
from TransmissionNodeSample import TransmissionNodeSample
from TransmissionNodeSample_TransmissionFile import TransmissionNodeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionNodeSample_PangeaSim(TransmissionNodeSample):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        assert "ContactNetworkGenerator_PangeaSim" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_PangeaSim module"
        assert "EndCriteria_PangeaSim" in str(MF.modules['EndCriteria']), "Must use EndCriteria_PangeaSim module"
        assert "SeedSelection_PangeaSim" in str(MF.modules['SeedSelection']), "Must use SeedSelection_PangeaSim module"
        assert "TransmissionTimeSample_PangeaSim" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_PangeaSim module"

    def sample_nodes(time):
        return TransmissionNodeSample_TransmissionFile.sample_nodes(time)

    def check_contact_network(cn):
        pass