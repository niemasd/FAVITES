#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016).
'''
from TransmissionNodeSample import TransmissionNodeSample
from TransmissionNodeSample_TransmissionFile import TransmissionNodeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionNodeSample_GEMF(TransmissionNodeSample):
    def init():
        assert "GEMF" in str(MF.modules['TransmissionTimeSample']), "Must use a GEMF TransmissionTimeSample module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"

    def sample_nodes(time):
        if not GC.gemf_ready:
            MF.modules['TransmissionTimeSample'].prep_GEMF()
        return TransmissionNodeSample_TransmissionFile.sample_nodes(time)