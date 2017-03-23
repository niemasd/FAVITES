#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module, where transmissions follow the SI model
'''
from TransmissionNodeSample import TransmissionNodeSample
from TransmissionNodeSample_TransmissionFile import TransmissionNodeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionNodeSample_SIGEMF(TransmissionNodeSample):
    def init():
        assert "TransmissionTimeSample_SIGEMF" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_SIGEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        # handle parameter checking in TransmissionTimeSample_SIGEMF

    def sample_nodes(time):
        if not GC.gemf_ready:
            MF.modules['TransmissionTimeSample'].prep_GEMF()
        return TransmissionNodeSample_TransmissionFile.sample_nodes(time)