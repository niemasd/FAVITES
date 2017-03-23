#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module, where transmissions follow the SI model
'''
from TransmissionNodeSample import TransmissionNodeSample
from TransmissionNodeSample_SISGEMF import TransmissionNodeSample_SISGEMF
import modules.FAVITES_ModuleFactory as MF

class TransmissionNodeSample_SIGEMF(TransmissionNodeSample):
    def init():
        assert "TransmissionTimeSample_SIGEMF" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_SIGEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        # handle parameter checking in TransmissionTimeSample_SIGEMF

    def sample_nodes(time):
        return TransmissionNodeSample_SISGEMF.sample_nodes(time)