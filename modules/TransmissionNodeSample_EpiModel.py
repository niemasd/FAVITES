#! /usr/bin/env python3
'''
Niema Moshiri 2019

"TransmissionTimeSample" module, where the epidemic is simulated using EpiModel
'''
from TransmissionNodeSample import TransmissionNodeSample
from TransmissionNodeSample_TransmissionFile import TransmissionNodeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionNodeSample_EpiModel(TransmissionNodeSample):
    def cite():
        return GC.CITATION_EPIMODEL

    def init():
        assert "ContactNetworkGenerator_EpiModel" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_EpiModel module"
        assert "EndCriteria_EpiModel" in str(MF.modules['EndCriteria']), "Must use EndCriteria_EpiModel module"
        assert "SeedSelection_EpiModel" in str(MF.modules['SeedSelection']), "Must use SeedSelection_EpiModel module"
        assert "TransmissionTimeSample_EpiModel" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_EpiModel module"

    def check_contact_network(cn):
        assert not cn.is_directed(), "GEMF does not currently handle directed contact networks properly. Please use an undirected contact network"

    def sample_nodes(time):
        return TransmissionNodeSample_TransmissionFile.sample_nodes(time)