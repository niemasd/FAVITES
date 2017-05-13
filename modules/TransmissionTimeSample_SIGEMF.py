#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the SI model.
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_SISGEMF import TransmissionTimeSample_SISGEMF
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_SIGEMF(TransmissionTimeSample):
    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        GC.sis_beta = float(GC.si_beta)
        assert GC.sis_beta >= 0, "si_beta must be at least 0"
        GC.sis_delta = 0
        TransmissionTimeSample_SISGEMF.init()

    def prep_GEMF():
        TransmissionTimeSample_SISGEMF.prep_GEMF()

    def sample_time():
        return TransmissionTimeSample_SISGEMF.sample_time()