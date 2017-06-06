#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the SI model, but where individuals can be
"seed infected" (i.e., infected from outside the contact network) after time 0.
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_SISGEMF import TransmissionTimeSample_SISGEMF
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_SIGEMF(TransmissionTimeSample):
    def cite():
        return GC.CITATION_GEMF

    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        GC.sis_beta_seed = float(GC.si_beta_seed)
        assert GC.sis_beta_seed >= 0, "si_beta_seed must be at least 0"
        GC.sis_beta_by_i = float(GC.si_beta_by_i)
        assert GC.sis_beta_by_i >= 0, "si_beta_by_i must be at least 0"
        GC.sis_delta = 0
        TransmissionTimeSample_SISGEMF.init()

    def prep_GEMF():
        TransmissionTimeSample_SISGEMF.prep_GEMF()

    def sample_time():
        return TransmissionTimeSample_SISGEMF.sample_time()