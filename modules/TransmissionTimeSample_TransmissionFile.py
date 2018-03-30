#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is read from a
file
'''
from TransmissionTimeSample import TransmissionTimeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_TransmissionFile(TransmissionTimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "ContactNetworkGenerator_File" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_File module"
        assert "EndCriteria_TransmissionFile" in str(MF.modules['EndCriteria']), "Must use EndCriteria_TransmissionFile module"
        assert "SeedSelection_TransmissionFile" in str(MF.modules['SeedSelection']), "Must use SeedSelection_TransmissionFile module"
        assert "TransmissionNodeSample_TransmissionFile" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_TransmissionFile module"
        # SeedSelection_TransmissionFile sets everything up

    def sample_time():
        return GC.transmission_file[GC.transmission_num][2]