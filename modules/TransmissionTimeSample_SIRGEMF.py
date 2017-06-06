#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the SIR model, but where individuals can be
"seed infected" (i.e., infected from outside the contact network) after time 0.
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_SVITRGEMF import TransmissionTimeSample_SVITRGEMF
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from datetime import datetime
from subprocess import call
from os.path import expanduser
from os import chdir,getcwd,makedirs
from sys import stderr

class TransmissionTimeSample_SIRGEMF(TransmissionTimeSample):
    def cite():
        return GC.CITATION_GEMF

    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        GC.svitr_s_to_v = 0
        GC.svitr_i_to_t = 0
        GC.svitr_t_to_r = 0
        GC.svitr_beta_by_t = 0
        GC.svitr_beta_seed = float(GC.sir_beta_seed)
        assert GC.svitr_beta_seed >= 0, "sir_beta_seed must be at least 0"
        GC.svitr_beta_by_i = float(GC.sir_beta_by_i)
        assert GC.svitr_beta_by_i >= 0, "sir_beta_by_i must be at least 0"
        GC.svitr_delta = float(GC.sir_delta)
        assert GC.svitr_delta >= 0, "sir_delta must be at least 0"
        TransmissionTimeSample_SVITRGEMF.init()

    def prep_GEMF():
        TransmissionTimeSample_SVITRGEMF.prep_GEMF()

    def sample_time():
        return TransmissionTimeSample_SVITRGEMF.sample_time()